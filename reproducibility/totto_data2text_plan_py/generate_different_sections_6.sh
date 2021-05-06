#!/bin/bash
BASE=/home/ruslan_yermakov/nlg-ra/reproducibility/totto_data2text_plan_py/paper_code_section6
IDENTIFIER=cc
GPUID=0

# roto_stage1_acc_18.9744_ppl_30.9805_e4.pt       roto_stage2_acc_52.0487_ppl_10.3840_e4.pt

# roto_stage1_acc_21.2229_ppl_73.1081_e6.pt       roto_stage2_acc_57.8079_ppl_7.8213_e6.pt

# roto_stage1_acc_24.0631_ppl_217.8215_e8.pt      roto_stage2_acc_60.0880_ppl_7.3363_e8.pt

# roto_stage1_acc_25.0099_ppl_592.4188_e10.pt     roto_stage2_acc_62.2316_ppl_7.1621_e10.pt

# roto_stage1_acc_26.2130_ppl_2519.1899_e12.pt    roto_stage2_acc_64.0868_ppl_6.8235_e12.pt

# roto_stage1_acc_27.7318_ppl_8031.7282_e15.pt    roto_stage2_acc_65.3502_ppl_6.7793_e14.pt

# roto_stage1_acc_27.9882_ppl_5882.3857_e14.pt    roto_stage2_acc_65.6575_ppl_7.1781_e16.pt

# roto_stage1_acc_29.0730_ppl_80313.8291_e18.pt   roto_stage2_acc_66.2797_ppl_6.9690_e17.pt

# roto_stage1_acc_29.1519_ppl_82949.3649_e20.pt   roto_stage2_acc_66.5566_ppl_7.0834_e19.pt

# roto_stage1_acc_29.2899_ppl_137038.6017_e23.pt  roto_stage2_acc_66.8564_ppl_7.2482_e20.pt

# roto_stage1_acc_29.6450_ppl_135288.3505_e24.pt  roto_stage2_acc_67.2395_ppl_7.6808_e24.pt



MODEL_PATH_raw=$BASE/gen_model/cc/

for MODEL_ONE in roto_stage1_acc_18.9744_ppl_30.9805_e4.pt roto_stage1_acc_21.2229_ppl_73.1081_e6.pt roto_stage1_acc_24.0631_ppl_217.8215_e8.pt roto_stage1_acc_26.2130_ppl_2519.1899_e12.pt roto_stage1_acc_27.9882_ppl_5882.3857_e14.pt roto_stage1_acc_29.0730_ppl_80313.8291_e18.pt roto_stage1_acc_29.1519_ppl_82949.3649_e20.pt roto_stage1_acc_29.6450_ppl_135288.3505_e24.pt

do
    
    MODEL_PATH=$MODEL_PATH_raw$MODEL_ONE
    
    for MODEL_TWO in roto_stage2_acc_52.0487_ppl_10.3840_e4.pt roto_stage2_acc_57.8079_ppl_7.8213_e6.pt roto_stage2_acc_60.0880_ppl_7.3363_e8.pt roto_stage2_acc_62.2316_ppl_7.1621_e10.pt roto_stage2_acc_64.0868_ppl_6.8235_e12.pt roto_stage2_acc_65.3502_ppl_6.7793_e14.pt roto_stage2_acc_65.6575_ppl_7.1781_e16.pt roto_stage2_acc_66.8564_ppl_7.2482_e20.pt roto_stage2_acc_67.2395_ppl_7.6808_e24.pt
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