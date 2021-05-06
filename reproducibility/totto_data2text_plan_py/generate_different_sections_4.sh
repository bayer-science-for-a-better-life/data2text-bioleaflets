#!/bin/bash
BASE=/home/ruslan_yermakov/nlg-ra/reproducibility/totto_data2text_plan_py/paper_code_section4
IDENTIFIER=cc
GPUID=0

# roto_stage1_acc_16.2348_ppl_43.5144_e4.pt    roto_stage2_acc_55.8649_ppl_8.5781_e4.pt

# roto_stage1_acc_27.2288_ppl_33.5748_e6.pt    roto_stage2_acc_62.0948_ppl_6.1372_e6.pt

# roto_stage1_acc_34.8958_ppl_40.2558_e8.pt    roto_stage2_acc_66.5604_ppl_5.0249_e8.pt

# roto_stage1_acc_39.8127_ppl_65.8964_e10.pt   roto_stage2_acc_69.6220_ppl_4.4603_e10.pt

# roto_stage1_acc_42.4155_ppl_89.4504_e12.pt   roto_stage2_acc_72.4680_ppl_4.0392_e12.pt

# roto_stage1_acc_44.4765_ppl_252.6456_e14.pt  roto_stage2_acc_74.3791_ppl_3.8232_e14.pt

# roto_stage1_acc_45.6719_ppl_305.0665_e16.pt  roto_stage2_acc_75.5711_ppl_3.6574_e16.pt

# roto_stage1_acc_46.8437_ppl_263.3710_e18.pt  roto_stage2_acc_76.7062_ppl_3.5186_e18.pt

# roto_stage1_acc_47.7506_ppl_378.7944_e20.pt  roto_stage2_acc_77.5403_ppl_3.5106_e20.pt

# roto_stage1_acc_48.2452_ppl_326.2381_e22.pt  roto_stage2_acc_78.4621_ppl_3.3857_e22.pt

# roto_stage1_acc_48.6515_ppl_340.6895_e24.pt  roto_stage2_acc_78.9941_ppl_3.3024_e24.pt


MODEL_PATH_raw=$BASE/gen_model/cc/

for MODEL_ONE in roto_stage1_acc_16.2348_ppl_43.5144_e4.pt roto_stage1_acc_27.2288_ppl_33.5748_e6.pt roto_stage1_acc_34.8958_ppl_40.2558_e8.pt roto_stage1_acc_39.8127_ppl_65.8964_e10.pt roto_stage1_acc_42.4155_ppl_89.4504_e12.pt roto_stage1_acc_45.6719_ppl_305.0665_e16.pt roto_stage1_acc_46.8437_ppl_263.3710_e18.pt roto_stage1_acc_47.7506_ppl_378.7944_e20.pt roto_stage1_acc_48.6515_ppl_340.6895_e24.pt

do
    
    MODEL_PATH=$MODEL_PATH_raw$MODEL_ONE
    
    for MODEL_TWO in roto_stage2_acc_55.8649_ppl_8.5781_e4.pt roto_stage2_acc_62.0948_ppl_6.1372_e6.pt roto_stage2_acc_66.5604_ppl_5.0249_e8.pt roto_stage2_acc_69.6220_ppl_4.4603_e10.pt roto_stage2_acc_72.4680_ppl_4.0392_e12.pt roto_stage2_acc_74.3791_ppl_3.8232_e14.pt roto_stage2_acc_76.7062_ppl_3.5186_e18.pt roto_stage2_acc_77.5403_ppl_3.5106_e20.pt roto_stage2_acc_78.4621_ppl_3.3857_e22.pt roto_stage2_acc_78.9941_ppl_3.3024_e24.pt
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