import numpy as np

from transformers import T5Tokenizer, BartTokenizer

from evaluations.calc_metrics import (
    calc_bleu,
    calc_sacrebleu
    )

# init HF tokenizers
T5_tokenizer = T5Tokenizer.from_pretrained('t5-base')
BART_tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')

## T5 Model

# read generated sections
PATH_TEST_GENERATED = '/home/pilot/bayer-intern/data2text-bioleaflets/results/T5_plain/outputs_seed_1/test_generations_beam_1.txt'
with open(PATH_TEST_GENERATED) as f:
    test_generated_T5_seed1 = [line.strip() for line in f]

# read test dataset
PATH_TEST_TARGET = '/home/pilot/bayer-intern/data2text-bioleaflets/scripts/data/plain/test.target'
with open(PATH_TEST_TARGET) as f:
    gold_reference_T5 = [line.strip() for line in f]

T5_sacrebleu_result = calc_sacrebleu(gold_references=gold_reference_T5.copy(),
                                     model_generations=test_generated_T5_seed1.copy(),
                                     truncation=True,
                                     model_tokenizer=T5_tokenizer
                                     )

print("SacreBLEU T5: ", T5_sacrebleu_result['score'])

T5_bleu_result = calc_bleu(gold_references=gold_reference_T5.copy(),
                           model_generations=test_generated_T5_seed1.copy(),
                           truncation=True,
                           model_tokenizer=T5_tokenizer
                           )

print("BLEU T5: ", T5_bleu_result['bleu'])

## Content Planner

# read generated sections
PATH_TEST_GENERATED = '/home/pilot/bayer-intern/data2text-bioleaflets/results/content_planner/all_generations_Content_Planner.txt'
with open(PATH_TEST_GENERATED) as f:
    CP_generations = [line.strip() for line in f]

# read test dataset
PATH_TEST_TARGET = '/home/pilot/bayer-intern/data2text-bioleaflets/results/content_planner/all_references_Content_Planner.txt'
with open(PATH_TEST_TARGET) as f:
    CP_references = [line.strip() for line in f]

CP_sacrebleu_result = calc_sacrebleu(gold_references=CP_references.copy(),
                                     model_generations=CP_generations.copy(),
                                     truncation=False,
                                     model_tokenizer=None
                                     )

print("SacreBLEU CP: ", CP_sacrebleu_result['score'])

CP_bleu_result = calc_bleu(gold_references=CP_references.copy(),
                           model_generations=CP_generations.copy(),
                           truncation=False,
                           model_tokenizer=None
                           )

print("BLEU CP: ", CP_bleu_result['bleu'])




