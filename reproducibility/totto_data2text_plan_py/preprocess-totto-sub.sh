BASE=~/ToTTo
IDENTIFIER=subtable

rm -rf ~/ToTTo/preprocess/
mkdir $BASE/preprocess/
python27 preprocess.py -train_src1 $BASE/${IDENTIFIER}_trainsrc.txt -train_tgt1 $BASE/${IDENTIFIER}_traincontent_plan.txt -train_src2 $BASE/${IDENTIFIER}_traincontent_plan_verbose.txt -train_tgt2 $BASE/${IDENTIFIER}_traintgt.txt -valid_src1 $BASE/${IDENTIFIER}_valsrc.txt -valid_tgt1 $BASE/${IDENTIFIER}_valcontent_plan.txt -valid_src2 $BASE/${IDENTIFIER}_valcontent_plan_verbose.txt -valid_tgt2 $BASE/${IDENTIFIER}_valtgt.txt -save_data $BASE/preprocess/totto-sub -src_seq_length 1000 -tgt_seq_length 1000 -dynamic_dict -train_ptr $BASE/${IDENTIFIER}_trainpointers.txt

