MODEL_PATH=~/totto/gen_model/main/totto_stage1_acc_51.5438_ppl_5.4483_e20.pt
MODEL_PATH2=~/totto/gen_model/main/totto_stage2_acc_75.7726_ppl_3.6893_e10.pt
GPUID=0
IDENTIFIER="e20"
BASE=~/totto

TEST="test_src_raw.txt"
VAL="val_src_raw.txt"

# Generate Content Plan Indices.
# python27 translate.py -model $MODEL_PATH -src1 $BASE/$TEST -output $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt -batch_size 1 -max_length 30 -gpu $GPUID -min_length 8 -stage1 -beam_size 5
# python27 translate.py -model $MODEL_PATH -src1 $BASE/$VAL -output $BASE/gen/roto_stage1_$IDENTIFIER-beam5_val_gens.txt -batch_size 1 -max_length 30 -gpu $GPUID -min_length 8 -stage1 -beam_size 4

# Replace empty lines.
# sed 's/^\s*$/0 0 0 0 0/' $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt -i
# sed 's/^\s*$/0 0 0 0 0/' $BASE/gen/roto_stage1_$IDENTIFIER-beam5_val_gens.txt -i

# Convert into lexicalized plan. 
# echo "test conversion"
# python27 scripts/create_content_plan_from_index.py $BASE/$TEST $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt $BASE/transform_gen/roto_stage1_$IDENTIFIER-beam5_test_gens.h5-tuples.txt $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_test_gens.txt
# echo "val conversion"
# python27 scripts/create_content_plan_from_index.py $BASE/$VAL $BASE/gen/roto_stage1_$IDENTIFIER-beam5_val_gens.txt $BASE/transform_gen/roto_stage1_$IDENTIFIER-beam5_val_gens.h5-tuples.txt $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_val_gens.txt
 
python27 translate.py -model $MODEL_PATH -model2 $MODEL_PATH2 -src1 $BASE/$TEST -tgt1 $BASE/gen/roto_stage1_$IDENTIFIER-beam5_test_gens.txt -src2 $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_test_gens.txt -output $BASE/gen/roto_stage2_$IDENTIFIER-beam5_test_gens.txt -batch_size 1 -max_length 50 -min_length 5 -gpu $GPUID 
python27 translate.py -model $MODEL_PATH -model2 $MODEL_PATH2 -src1 $BASE/$VAL -tgt1 $BASE/gen/roto_stage1_$IDENTIFIER-beam5_val_gens.txt -src2 $BASE/gen/roto_stage1_inter_$IDENTIFIER-beam5_val_gens.txt -output $BASE/gen/roto_stage2_$IDENTIFIER-beam5_val_gens.txt -batch_size 1 -max_length 50 -min_length 5  -gpu $GPUID
