BASE=~/totto
IDENTIFIER=cc

rm -rf ~/totto/preprocess/
mkdir $BASE/preprocess
python27 preprocess.py -train_src1 $BASE/train_src.txt -train_tgt1 $BASE/train_content_plan.txt -train_src2 $BASE/train_content_plan_verbose.txt -train_tgt2 $BASE/train_tgt.txt -valid_src1 $BASE/val_src.txt -valid_tgt1 $BASE/val_content_plan.txt -valid_src2 $BASE/val_content_plan_verbose.txt -valid_tgt2 $BASE/val_tgt.txt -save_data $BASE/preprocess/totto -src_seq_length 1000 -tgt_seq_length 1000 -dynamic_dict -train_ptr $BASE/train_pointers.txt

