MODEL_PATH=~/totto/gen_model/main/totto_stage1_acc_51.5438_ppl_5.4483_e20.pt
GPUID=0
IDENTIFIER="e20"
BASE=~/totto

python27 translate.py -model $MODEL_PATH -src1 $BASE/test_src_raw.txt -output $BASE/gen/roto_stage1_$IDENTIFIER-beam5_gens.txt -batch_size 1 -max_length 80 -gpu $GPUID -min_length 3 -stage1 -batch_size 3

