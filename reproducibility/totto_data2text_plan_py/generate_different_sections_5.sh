#!/bin/bash
BASE=/home/ruslan_yermakov/nlg-ra/reproducibility/totto_data2text_plan_py/paper_code_section5
IDENTIFIER=cc
GPUID=0

# roto_stage1_acc_45.9716_ppl_16.4820_e6.pt   roto_stage2_acc_75.0910_ppl_3.3749_e4.pt

# roto_stage1_acc_47.3934_ppl_7.2179_e5.pt    roto_stage2_acc_77.4905_ppl_2.9508_e6.pt

# roto_stage1_acc_48.3412_ppl_14.7150_e8.pt   roto_stage2_acc_79.6966_ppl_2.7064_e8.pt

# roto_stage1_acc_49.2891_ppl_31.8245_e15.pt  roto_stage2_acc_80.4861_ppl_2.6043_e10.pt

# roto_stage1_acc_50.5924_ppl_14.3700_e12.pt  roto_stage2_acc_81.3685_ppl_2.5736_e12.pt

# roto_stage1_acc_50.5924_ppl_58.9799_e24.pt  roto_stage2_acc_82.2355_ppl_2.5564_e14.pt

# roto_stage1_acc_50.8294_ppl_16.4651_e13.pt  roto_stage2_acc_82.5064_ppl_2.5319_e15.pt

# roto_stage1_acc_51.7773_ppl_35.6314_e19.pt  roto_stage2_acc_82.6457_ppl_2.6186_e18.pt

# roto_stage1_acc_52.1327_ppl_21.0581_e16.pt  roto_stage2_acc_82.7541_ppl_2.6229_e17.pt

# roto_stage1_acc_52.8436_ppl_32.1332_e18.pt  roto_stage2_acc_82.8083_ppl_2.7408_e23.pt

# roto_stage1_acc_54.0284_ppl_51.3860_e20.pt  roto_stage2_acc_83.0095_ppl_2.8547_e25.pt



MODEL_PATH_raw=$BASE/gen_model/cc/

for MODEL_ONE in roto_stage1_acc_45.9716_ppl_16.4820_e6.pt roto_stage1_acc_47.3934_ppl_7.2179_e5.pt roto_stage1_acc_48.3412_ppl_14.7150_e8.pt roto_stage1_acc_49.2891_ppl_31.8245_e15.pt roto_stage1_acc_50.5924_ppl_14.3700_e12.pt roto_stage1_acc_50.8294_ppl_16.4651_e13.pt roto_stage1_acc_51.7773_ppl_35.6314_e19.pt roto_stage1_acc_52.1327_ppl_21.0581_e16.pt roto_stage1_acc_52.8436_ppl_32.1332_e18.pt roto_stage1_acc_54.0284_ppl_51.3860_e20.pt

do
    
    MODEL_PATH=$MODEL_PATH_raw$MODEL_ONE
    
    for MODEL_TWO in roto_stage2_acc_75.0910_ppl_3.3749_e4.pt roto_stage2_acc_77.4905_ppl_2.9508_e6.pt roto_stage2_acc_79.6966_ppl_2.7064_e8.pt roto_stage2_acc_80.4861_ppl_2.6043_e10.pt roto_stage2_acc_81.3685_ppl_2.5736_e12.pt roto_stage2_acc_82.2355_ppl_2.5564_e14.pt roto_stage2_acc_82.5064_ppl_2.5319_e15.pt roto_stage2_acc_82.6457_ppl_2.6186_e18.pt roto_stage2_acc_82.7541_ppl_2.6229_e17.pt roto_stage2_acc_82.8083_ppl_2.7408_e23.pt
    do  
        MODEL_PATH2=$MODEL_PATH_raw$MODEL_TWO
        
        echo $MODEL_PATH
        echo $MODEL_PATH2

        python translate.py -model $MODEL_PATH -src1 $BASE/test/src_test.txt -output $BASE/all_models_generations/stage1_$MODEL_ONE$MODEL_TWO.txt -batch_size 1 -max_length 80 -gpu $GPUID -min_length 35 -stage1

        python scripts/create_content_plan_from_index.py $BASE/test/src_test.txt $BASE/all_models_generations/stage1_$MODEL_ONE$MODEL_TWO.txt $BASE/transform_gen/roto_stage1_$IDENTIFIER-beam5_test_gens.h5-tuples.txt $BASE/all_models_generations/stage1_inter_$MODEL_ONE$MODEL_TWO.txt

        python translate.py -model $MODEL_PATH -model2 $MODEL_PATH2 -src1 $BASE/test/src_test.txt -tgt1 $BASE/all_models_generations/stage1_$MODEL_ONE$MODEL_TWO.txt -src2 $BASE/all_models_generations/stage1_inter_$MODEL_ONE$MODEL_TWO.txt -output $BASE/all_models_generations/stage2_$MODEL_ONE$MODEL_TWO.txt -batch_size 1 -max_length 850 -min_length 150 -gpu $GPUID
        
        
        # echo $BASE/all_models_generations/stage2_$MODEL_ONE$MODEL_TWO.txt
        
        # echo "======================="

    done

done

# MODEL_PATH=$BASE/gen_model/cc/roto_stage1_acc_35.0259_ppl_22302.7258_e15.pt

# MODEL_PATH2=$BASE/gen_model/cc/roto_stage2_acc_59.6033_ppl_11.8064_e17.pt

# python translate.py -model $MODEL_PATH -src1 $BASE/test/src_test.txt -output $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt -batch_size 1 -max_length 80 -gpu $GPUID -min_length 35 -stage1

# python scripts/create_content_plan_from_index.py $BASE/test/src_test.txt $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt $BASE/transform_gen/roto_stage1_$IDENTIFIER-beam5_test_gens.h5-tuples.txt  $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_test_gens.txt

# python translate.py -model $MODEL_PATH -model2 $MODEL_PATH2 -src1 $BASE/test/src_test.txt -tgt1 $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt -src2 $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_test_gens.txt -output $BASE/gen/roto_stage2_$IDENTIFIER-beam5_test_gens.txt -batch_size 1 -max_length 850 -min_length 150 -gpu $GPUID