#!/bin/bash

# activate conda env
conda activate t5_text2text

# change directory where transformers python files are
cd /home/angelo_ziletti/nlg-ra/transformers/examples/seq2seq/

### T5_plain_type

# indicate path to input dir
export DATA_DIR="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_plain/input_data"

# indicate path to output dir
export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_plain/outputs_seed_5"

# fine-tuning
python finetune_trainer.py --model_name_or_path t5-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 2000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 1e-3 --seed 5

# evaluation (test generations)
./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_plain/outputs_seed_6"

# fine-tuning
python finetune_trainer.py --model_name_or_path t5-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 2000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 1e-3 --seed 6

# evaluation (test generations)
./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_plain/outputs_seed_7"

# fine-tuning
python finetune_trainer.py --model_name_or_path t5-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 2000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 1e-3 --seed 7

# evaluation (test generations)
./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

### T5_condition_section_type

# indicate path to input dir
export DATA_DIR="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_condition/input_data"

# indicate path to output dir
export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_condition/outputs_seed_5"

# fine-tuning
python finetune_trainer.py --model_name_or_path t5-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 2000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 1e-3 --seed 5

# evaluation (test generations)
./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_condition/outputs_seed_6"

# fine-tuning
python finetune_trainer.py --model_name_or_path t5-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 2000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 1e-3 --seed 6

# evaluation (test generations)
./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_condition/outputs_seed_7"

# fine-tuning
python finetune_trainer.py --model_name_or_path t5-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 2000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 1e-3 --seed 7

# evaluation (test generations)
./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

### T5_condition_section_title

# indicate path to input dir
#export DATA_DIR="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_condition_semantics/input_data"

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_condition_semantics/outputs_seed_2"

# fine-tuning
#python finetune_trainer.py --model_name_or_path t5-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 2000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 1e-3 --seed 2

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/T5_condition_semantics/outputs_seed_3"

# fine-tuning
#python finetune_trainer.py --model_name_or_path t5-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 2000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 1e-3 --seed 3

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1


### BART_base_section_type

# indicate path to input dir
#export DATA_DIR="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_base/input_data"

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_base/outputs_seed_5"

# fine-tuning BART
#python finetune_trainer.py --model_name_or_path facebook/bart-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 1000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 5e-5 --seed 5

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_base/outputs_seed_6"

# fine-tuning BART
#python finetune_trainer.py --model_name_or_path facebook/bart-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 1000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 5e-5 --seed 6

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_base/outputs_seed_7"

# fine-tuning BART
#python finetune_trainer.py --model_name_or_path facebook/bart-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 1000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 5e-5 --seed 7

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

### BART_condition_section_type

# indicate path to input dir
#export DATA_DIR="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_condition/input_data"

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_condition/outputs_seed_5"

# fine-tuning BART
#python finetune_trainer.py --model_name_or_path facebook/bart-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 1000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 5e-5 --seed 5

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_condition/outputs_seed_6"

# fine-tuning BART
#python finetune_trainer.py --model_name_or_path facebook/bart-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 1000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 5e-5 --seed 6

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_condition/outputs_seed_7"

# fine-tuning BART
#python finetune_trainer.py --model_name_or_path facebook/bart-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 1000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 5e-5 --seed 7

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

### BART_condition_section_title

# indicate path to input dir
#export DATA_DIR="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_condition_semantics/input_data"

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_condition_semantics/outputs_seed_2"

# fine-tuning BART
#python finetune_trainer.py --model_name_or_path facebook/bart-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 1000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 5e-5 --seed 2

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1

# indicate path to output dir
#export DATA_DIR_OUT="/home/angelo_ziletti/nlg-ra/T5_experiments/BART_condition_semantics/outputs_seed_3"

# fine-tuning BART
#python finetune_trainer.py --model_name_or_path facebook/bart-base --data_dir $DATA_DIR --output_dir $DATA_DIR_OUT --n_train -1 --n_val -1 --n_test -1 --max_target_length 512 --val_max_target_length 512 --test_max_target_length 512 --task summarization --save_steps 1000 --num_train_epochs 20 --save_total_limit 4 --do_train True --do_eval False --do_predict False --predict_with_generate False --evaluation_strategy no --gradient_accumulation_steps 16 --per_device_train_batch_size 2 --per_device_eval_batch_size 8 --learning_rate 5e-5 --seed 3

# evaluation (test generations)
#./run_eval.py $DATA_DIR_OUT $DATA_DIR/test.source $DATA_DIR_OUT/test_generations_beam_1.txt --reference_path $DATA_DIR/test.target --score_path $DATA_DIR_OUT/test_scores_beam_1.json --device cuda --bs 16 --num_beams 1
