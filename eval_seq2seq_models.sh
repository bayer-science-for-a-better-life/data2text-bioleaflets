#!/bin/bash

# goal - given fine-tuned model - generate text with different beam_size

# activate conda env
# conda activate t5_text2text

# change directory where transformers python files are
cd /home/ruslan_yermakov/nlg-ra/transformers/examples/seq2seq/

# indicate path to dir
export DATA_DIR="/home/ruslan_yermakov/nlg-ra/T5_experiments/T5_plain/input_data"

# path where model is saved
# export DATA_DIR_OUT="/home/ruslan_yermakov/nlg-ra/T5_experiments/T5_plain/hp_5e_5_1"
export DATA_DIR_OUT="/home/ruslan_yermakov/nlg-ra/T5_experiments/T5_plain/hp_1e_5_1_1/checkpoint-4000"


# text generation with different beam size

./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_5.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_5.json --device cuda --bs 16 --num_beams 5

./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_10.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_10.json --device cuda --bs 8 --num_beams 10
