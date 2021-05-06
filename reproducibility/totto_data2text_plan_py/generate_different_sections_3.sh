#!/bin/bash
BASE=/home/ruslan_yermakov/nlg-ra/reproducibility/totto_data2text_plan_py/paper_code_section3
IDENTIFIER=cc
GPUID=0

# roto_stage1_acc_10.0572_ppl_124.7271_e5.pt       roto_stage2_acc_49.0364_ppl_12.3752_e4.pt

# roto_stage1_acc_12.5715_ppl_435.3259_e7.pt       roto_stage2_acc_54.0132_ppl_9.7249_e6.pt

# roto_stage1_acc_15.1310_ppl_2240.1134_e9.pt      roto_stage2_acc_57.1011_ppl_8.7496_e8.pt

# roto_stage1_acc_16.3806_ppl_3231.8913_e10.pt     roto_stage2_acc_59.1353_ppl_8.0293_e10.pt

# roto_stage1_acc_17.8711_ppl_73536.6477_e14.pt    roto_stage2_acc_60.8357_ppl_7.6152_e12.pt

# roto_stage1_acc_18.0217_ppl_31625.5055_e13.pt    roto_stage2_acc_62.0284_ppl_7.0556_e14.pt

# roto_stage1_acc_19.2412_ppl_403282.2728_e18.pt   roto_stage2_acc_62.8682_ppl_7.1170_e16.pt

# roto_stage1_acc_19.6477_ppl_373368.3620_e19.pt   roto_stage2_acc_63.6298_ppl_7.0089_e18.pt

# roto_stage1_acc_19.9789_ppl_198537.7377_e20.pt   roto_stage2_acc_64.2781_ppl_7.0670_e20.pt

# roto_stage1_acc_21.0479_ppl_406631.4916_e23.pt   roto_stage2_acc_65.2105_ppl_6.7753_e22.pt

# roto_stage1_acc_9.6357_ppl_69.5646_e4.pt         roto_stage2_acc_65.8795_ppl_6.8667_e24.pt


MODEL_PATH_raw=$BASE/gen_model/cc/

for MODEL_ONE in roto_stage1_acc_10.0572_ppl_124.7271_e5.pt roto_stage1_acc_12.5715_ppl_435.3259_e7.pt roto_stage1_acc_15.1310_ppl_2240.1134_e9.pt roto_stage1_acc_17.8711_ppl_73536.6477_e14.pt roto_stage1_acc_18.0217_ppl_31625.5055_e13.pt roto_stage1_acc_19.2412_ppl_403282.2728_e18.pt roto_stage1_acc_19.9789_ppl_198537.7377_e20.pt roto_stage1_acc_21.0479_ppl_406631.4916_e23.pt roto_stage1_acc_9.6357_ppl_69.5646_e4.pt

do
    
    MODEL_PATH=$MODEL_PATH_raw$MODEL_ONE
    
    for MODEL_TWO in roto_stage2_acc_49.0364_ppl_12.3752_e4.pt roto_stage2_acc_54.0132_ppl_9.7249_e6.pt roto_stage2_acc_57.1011_ppl_8.7496_e8.pt roto_stage2_acc_60.8357_ppl_7.6152_e12.pt roto_stage2_acc_62.0284_ppl_7.0556_e14.pt roto_stage2_acc_62.8682_ppl_7.1170_e16.pt roto_stage2_acc_63.6298_ppl_7.0089_e18.pt roto_stage2_acc_65.2105_ppl_6.7753_e22.pt roto_stage2_acc_65.8795_ppl_6.8667_e24.pt
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