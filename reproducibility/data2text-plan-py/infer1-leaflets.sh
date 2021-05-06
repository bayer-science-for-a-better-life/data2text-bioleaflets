#!/bin/bash
MODEL_PATH=~/nlg-ra/reproducibility/totto_data2text_plan_py/bayer_dataset/gen_model/cc/roto_stage1_acc_30.6872_ppl_632.8499_e20.pt
GPUID=0
IDENTIFIER=cc
BASE=~/nlg-ra/reproducibility/totto_data2text_plan_py/bayer_dataset

mkdir $BASE/gen

### Batch Size should be 1 - do not ask why - with this shitty code it works only with batch size = 1

# During inference, we first generate the content plan
# python translate.py -model $MODEL_PATH -src1 $BASE/src_valid.txt -output $BASE/gen/roto_stage1_$IDENTIFIER-beam5_gens_val.txt -batch_size 10 -max_length 80 -gpu $GPUID -min_length 35 -stage1

python translate.py -model $MODEL_PATH -src1 $BASE/src_valid.txt -output $BASE/gen/roto_stage1_$IDENTIFIER-beam5_gens_val.txt -batch_size 1 -max_length 80 -gpu $GPUID -min_length 35 -stage1

# Output
# ('average src size', 25, 120)
# PRED AVG SCORE: -1.6007, PRED PPL: 4.9565

# Convert content plan into lexicalized plan
# changed a bit code in scripts/create_content_plan_from_index.py
python scripts/create_content_plan_from_index.py $BASE/src_valid.txt $BASE/gen/roto_stage1_$IDENTIFIER-beam5_gens_val.txt $BASE/transform_gen/roto_stage1_$IDENTIFIER-beam5_gens.h5-tuples.txt $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_gens_val.txt

# The output summary is generated using the command

python translate.py -model $MODEL_PATH -model2 $MODEL_PATH2 -src1 $BASE/src_valid.txt -tgt1 $BASE/gen/roto_stage1_$IDENTIFIER-beam5_gens_val.txt -src2 $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_gens_val.txt -output $BASE/gen/roto_stage2_$IDENTIFIER-beam5_gens_val.txt -batch_size 1 -max_length 850 -min_length 150 -gpu $GPUID


# PRED AVG SCORE: -0.5157, PRED PPL: 1.6748