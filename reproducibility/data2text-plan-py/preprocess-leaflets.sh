#!/bin/bash

BASE=~/nlg-ra/reproducibility/data2text-plan-py/bayer_dataset
IDENTIFIER=cc

rm -rf ~/nlg-ra/reproducibility/data2text-plan-py/bayer_dataset/preprocess/
mkdir $BASE/preprocess

python preprocess.py -train_src1 $BASE/src_train.txt -train_tgt1 $BASE/train_content_plan.txt -train_src2 $BASE/inter/train_content_plan.txt -train_tgt2 $BASE/tgt_train.txt -valid_src1 $BASE/src_valid.txt -valid_tgt1 $BASE/valid_content_plan.txt -valid_src2 $BASE/inter/valid_content_plan.txt -valid_tgt2 $BASE/tgt_valid.txt -save_data $BASE/preprocess/roto -src_seq_length 1000 -tgt_seq_length 1000 -dynamic_dict -train_ptr $BASE/train-roto-ptrs.txt