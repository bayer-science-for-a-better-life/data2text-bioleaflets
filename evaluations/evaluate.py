import numpy as np

from transformers import T5Tokenizer, BartTokenizer

from evaluations.calc_metrics import (
    calc_bleu,
    calc_sacrebleu,
    calc_rouge
    )

# init HF tokenizers
T5_tokenizer = T5Tokenizer.from_pretrained('t5-base')
BART_tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')

# Example of evaluation with SacreBLEU

# read generated sections
PATH_TEST_GENERATED = 'path-to-generations'
with open(PATH_TEST_GENERATED) as f:
    test_generated_T5_seed1 = [line.strip() for line in f]

# read references dataset
PATH_TEST_TARGET = 'path-to-references'
with open(PATH_TEST_TARGET) as f:
    gold_reference_T5 = [line.strip() for line in f]

T5_sacrebleu_result = calc_sacrebleu(gold_references=gold_reference_T5.copy(),
                                     model_generations=test_generated_T5_seed1.copy(),
                                     truncation=True,
                                     model_tokenizer=T5_tokenizer
                                     )

print("SacreBLEU T5: ", T5_sacrebleu_result['score'])

# Example of evaluation with ROUGE-L


PATH_GENERATED = 'path-to-generations'
PATH_ORIGINAL = 'path-to-references'

# read all generations by BART
with open(PATH_GENERATED) as f:
    BART_generations = [line.strip() for line in f]

# read all references
with open(PATH_ORIGINAL) as f:
    BART_references = [line.strip() for line in f]

BART_rouge_result = calc_rouge(gold_references=BART_references.copy(),
                               model_generations=BART_generations.copy(),
                               truncation=True,
                               model_tokenizer=BART_tokenizer
                               )

print("ROUGE scores BART: ", BART_rouge_result)

