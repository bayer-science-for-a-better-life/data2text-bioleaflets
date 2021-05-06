#!/bin/bash
BASE=/home/ruslan_yermakov/nlg-ra/reproducibility/totto_data2text_plan_py/paper_code_section2
IDENTIFIER=cc
GPUID=0

# roto_stage1_acc_18.6016_ppl_57.3508_e4.pt      roto_stage2_acc_58.1691_ppl_7.1350_e4.pt

# roto_stage1_acc_27.6637_ppl_80.2429_e6.pt      roto_stage2_acc_63.5673_ppl_5.7638_e6.pt

#                                                roto_stage2_acc_66.5477_ppl_5.2388_e8.pt

# roto_stage1_acc_33.7186_ppl_1580.8918_e10.pt   roto_stage2_acc_68.2577_ppl_5.1150_e10.pt

# roto_stage1_acc_35.9094_ppl_2029.0636_e12.pt   roto_stage2_acc_70.1979_ppl_4.7599_e12.pt

# roto_stage1_acc_36.4901_ppl_5194.5648_e15.pt   roto_stage2_acc_71.8795_ppl_4.4200_e14.pt

# roto_stage1_acc_37.0651_ppl_2007.0101_e14.pt   roto_stage2_acc_73.1422_ppl_4.1846_e16.pt

# roto_stage1_acc_37.5827_ppl_6155.2643_e19.pt   roto_stage2_acc_73.9360_ppl_4.1326_e18.pt

# roto_stage1_acc_38.0714_ppl_11276.8573_e24.pt  roto_stage2_acc_74.6177_ppl_4.0631_e20.pt

# roto_stage1_acc_38.2957_ppl_8571.0033_e20.pt   roto_stage2_acc_75.0806_ppl_4.1052_e22.pt

# roto_stage1_acc_38.4452_ppl_18043.7361_e25.pt  roto_stage2_acc_75.7218_ppl_4.0301_e24.pt


MODEL_PATH_raw=$BASE/gen_model/cc/

for MODEL_ONE in roto_stage1_acc_18.6016_ppl_57.3508_e4.pt roto_stage1_acc_27.6637_ppl_80.2429_e6.pt roto_stage1_acc_33.7186_ppl_1580.8918_e10.pt roto_stage1_acc_35.9094_ppl_2029.0636_e12.pt roto_stage1_acc_36.4901_ppl_5194.5648_e15.pt roto_stage1_acc_37.5827_ppl_6155.2643_e19.pt roto_stage1_acc_38.2957_ppl_8571.0033_e20.pt roto_stage1_acc_38.0714_ppl_11276.8573_e24.pt

do
    
    MODEL_PATH=$MODEL_PATH_raw$MODEL_ONE
    
    for MODEL_TWO in roto_stage2_acc_58.1691_ppl_7.1350_e4.pt roto_stage2_acc_63.5673_ppl_5.7638_e6.pt roto_stage2_acc_66.5477_ppl_5.2388_e8.pt roto_stage2_acc_68.2577_ppl_5.1150_e10.pt roto_stage2_acc_70.1979_ppl_4.7599_e12.pt roto_stage2_acc_71.8795_ppl_4.4200_e14.pt roto_stage2_acc_73.1422_ppl_4.1846_e16.pt roto_stage2_acc_73.9360_ppl_4.1326_e18.pt roto_stage2_acc_74.6177_ppl_4.0631_e20.pt roto_stage2_acc_75.0806_ppl_4.1052_e22.pt roto_stage2_acc_75.7218_ppl_4.0301_e24.pt
    do  
        MODEL_PATH2=$MODEL_PATH_raw$MODEL_TWO
        
        echo $MODEL_PATH
        echo $MODEL_PATH2

        python translate.py -model $MODEL_PATH -src1 $BASE/test/src_test.txt -output $BASE/all_models_generations/stage1_$MODEL_ONE_$MODEL_TWO.txt -batch_size 1 -max_length 80 -gpu $GPUID -min_length 35 -stage1

        python scripts/create_content_plan_from_index.py $BASE/test/src_test.txt $BASE/all_models_generations/stage1_$MODEL_ONE_$MODEL_TWO.txt $BASE/transform_gen/roto_stage1_$IDENTIFIER-beam5_test_gens.h5-tuples.txt $BASE/all_models_generations/stage1_inter_$MODEL_ONE_$MODEL_TWO.txt

        python translate.py -model $MODEL_PATH -model2 $MODEL_PATH2 -src1 $BASE/test/src_test.txt -tgt1 $BASE/all_models_generations/stage1_$MODEL_ONE_$MODEL_TWO.txt -src2 $BASE/all_models_generations/stage1_inter_$MODEL_ONE_$MODEL_TWO.txt -output $BASE/all_models_generations/stage2_$MODEL_ONE$MODEL_TWO.txt -batch_size 1 -max_length 850 -min_length 150 -gpu $GPUID
        
        
        # echo $BASE/all_models_generations/stage2_$MODEL_ONE$MODEL_TWO.txt
        
        # echo "======================="

    done

done

# MODEL_PATH=$BASE/gen_model/cc/roto_stage1_acc_35.0259_ppl_22302.7258_e15.pt

# MODEL_PATH2=$BASE/gen_model/cc/roto_stage2_acc_59.6033_ppl_11.8064_e17.pt

# python translate.py -model $MODEL_PATH -src1 $BASE/test/src_test.txt -output $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt -batch_size 1 -max_length 80 -gpu $GPUID -min_length 35 -stage1

# python scripts/create_content_plan_from_index.py $BASE/test/src_test.txt $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt $BASE/transform_gen/roto_stage1_$IDENTIFIER-beam5_test_gens.h5-tuples.txt  $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_test_gens.txt

# python translate.py -model $MODEL_PATH -model2 $MODEL_PATH2 -src1 $BASE/test/src_test.txt -tgt1 $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt -src2 $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_test_gens.txt -output $BASE/gen/roto_stage2_$IDENTIFIER-beam5_test_gens.txt -batch_size 1 -max_length 850 -min_length 150 -gpu $GPUID