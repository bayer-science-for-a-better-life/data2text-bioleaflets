#!/bin/bash
BASE=/home/ruslan_yermakov/nlg-ra/reproducibility/totto_data2text_plan_py/paper_code_section1
IDENTIFIER=cc
GPUID=0

# roto_stage1_acc_19.7927_ppl_28.5086_e4.pt       roto_stage2_acc_35.9521_ppl_29.7960_e4.pt

# roto_stage1_acc_25.1295_ppl_1794.3449_e8.pt     roto_stage2_acc_45.1973_ppl_18.0023_e6.pt

# roto_stage1_acc_27.6425_ppl_148.5139_e7.pt      roto_stage2_acc_50.0673_ppl_14.7644_e8.pt

# roto_stage1_acc_29.6114_ppl_1711.5713_e9.pt     roto_stage2_acc_53.6178_ppl_13.3320_e10.pt

# roto_stage1_acc_31.4767_ppl_296253.7662_e23.pt  roto_stage2_acc_55.8835_ppl_12.2270_e12.pt

# roto_stage1_acc_32.1244_ppl_3109.0248_e11.pt    roto_stage2_acc_58.4400_ppl_11.5146_e14.pt

# roto_stage1_acc_32.3575_ppl_6049.1894_e12.pt    roto_stage2_acc_59.5425_ppl_11.1062_e16.pt

# roto_stage1_acc_32.4093_ppl_195303.1814_e25.pt  roto_stage2_acc_60.4453_ppl_11.3558_e18.pt

# roto_stage1_acc_33.9637_ppl_6288.3673_e14.pt    roto_stage2_acc_61.1528_ppl_11.1197_e19.pt

# roto_stage1_acc_35.0000_ppl_32561.3110_e16.pt   roto_stage2_acc_62.1945_ppl_10.8553_e22.pt

# roto_stage1_acc_35.8290_ppl_31546.7862_e18.pt   roto_stage2_acc_63.1928_ppl_10.9571_e24.pt
# roto_stage1_acc_35.9067_ppl_35537.7711_e19.pt   roto_stage2_acc_63.5010_ppl_11.3272_e25.pt


MODEL_PATH_raw=$BASE/gen_model/cc/

for MODEL_ONE in roto_stage1_acc_19.7927_ppl_28.5086_e4.pt roto_stage1_acc_25.1295_ppl_1794.3449_e8.pt roto_stage1_acc_27.6425_ppl_148.5139_e7.pt roto_stage1_acc_32.1244_ppl_3109.0248_e11.pt roto_stage1_acc_32.3575_ppl_6049.1894_e12.pt roto_stage1_acc_33.9637_ppl_6288.3673_e14.pt roto_stage1_acc_35.0000_ppl_32561.3110_e16.pt roto_stage1_acc_35.8290_ppl_31546.7862_e18.pt

do
    
    MODEL_PATH=$MODEL_PATH_raw$MODEL_ONE
    
    for MODEL_TWO in roto_stage2_acc_35.9521_ppl_29.7960_e4.pt roto_stage2_acc_45.1973_ppl_18.0023_e6.pt roto_stage2_acc_50.0673_ppl_14.7644_e8.pt roto_stage2_acc_55.8835_ppl_12.2270_e12.pt roto_stage2_acc_58.4400_ppl_11.5146_e14.pt roto_stage2_acc_59.5425_ppl_11.1062_e16.pt roto_stage2_acc_61.1528_ppl_11.1197_e19.pt roto_stage2_acc_62.1945_ppl_10.8553_e22.pt roto_stage2_acc_63.1928_ppl_10.9571_e24.pt roto_stage2_acc_63.5010_ppl_11.3272_e25.pt
    do  
        MODEL_PATH2=$MODEL_PATH_raw$MODEL_TWO
        
        echo $MODEL_PATH
        echo $MODEL_PATH2

        python translate.py -model $MODEL_PATH -src1 $BASE/test/src_test.txt -output $BASE/all_models_generations/stage1_$MODEL_ONE_$MODEL_TWO.txt -batch_size 1 -max_length 80 -gpu $GPUID -min_length 35 -stage1

        python scripts/create_content_plan_from_index.py $BASE/test/src_test.txt $BASE/all_models_generations/stage1_$MODEL_ONE_$MODEL_TWO.txt $BASE/transform_gen/roto_stage1_$IDENTIFIER-beam5_test_gens.h5-tuples.txt $BASE/all_models_generations/stage1_inter_$MODEL_ONE_$MODEL_TWO.txt

        python translate.py -model $MODEL_PATH -model2 $MODEL_PATH2 -src1 $BASE/test/src_test.txt -tgt1 $BASE/all_models_generations/stage1_$MODEL_ONE_$MODEL_TWO.txt -src2 $BASE/all_models_generations/stage1_inter_$MODEL_ONE_$MODEL_TWO.txt -output $BASE/all_models_generations/stage2_$MODEL_ONE$MODEL_TWO.txt -batch_size 1 -max_length 850 -min_length 150 -gpu $GPUID

    done

done

# MODEL_PATH=$BASE/gen_model/cc/roto_stage1_acc_35.0259_ppl_22302.7258_e15.pt

# MODEL_PATH2=$BASE/gen_model/cc/roto_stage2_acc_59.6033_ppl_11.8064_e17.pt

# python translate.py -model $MODEL_PATH -src1 $BASE/test/src_test.txt -output $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt -batch_size 1 -max_length 80 -gpu $GPUID -min_length 35 -stage1

# python scripts/create_content_plan_from_index.py $BASE/test/src_test.txt $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt $BASE/transform_gen/roto_stage1_$IDENTIFIER-beam5_test_gens.h5-tuples.txt  $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_test_gens.txt

# python translate.py -model $MODEL_PATH -model2 $MODEL_PATH2 -src1 $BASE/test/src_test.txt -tgt1 $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt -src2 $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_test_gens.txt -output $BASE/gen/roto_stage2_$IDENTIFIER-beam5_test_gens.txt -batch_size 1 -max_length 850 -min_length 150 -gpu $GPUID