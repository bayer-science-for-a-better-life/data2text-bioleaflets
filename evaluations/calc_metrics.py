from bert_score import BERTScorer

import datasets
import transformers
import pandas as pd
import numpy as np


def _truncate_reference_sections(references, model_tokenizer):
    """
    Truncate target sections so that the length of tokenized section <= 512

    *Note*: generations are at most 512 tokens in tokenized format (max_target_length = 512).
    For evaluations with word-overlap metrics (bleu, rouge), we need to also tokenize the reference sections
    in order to have comparable length.

    :param references: list of target sections
    :param model_tokenizer: HuggingFace Tokenizer
    :return: list of target truncated sections
    """

    # keep the count of truncated sections
    COUNT_SECTIONS_TRUNCATED = 0

    # save the truncated references in list
    truncated_references = []

    # for each section in references
    for ref_section in references:

        # tokenize with <model_tokenizer>
        ref_section_tokenized = model_tokenizer(ref_section)
        input_ids = ref_section_tokenized['input_ids']

        # truncate the tokenized ref_section if its length > 512
        if len(input_ids) > 512:

            COUNT_SECTIONS_TRUNCATED += 1

            # choose only <= 512
            input_ids = input_ids[:512]

            # decode back
            truncated_ref_text = model_tokenizer.decode(input_ids)

            truncated_references.append(truncated_ref_text)

        # otherwise just leave section as it is
        else:
            truncated_references.append(ref_section)

    print("Num. of sections truncated: ", COUNT_SECTIONS_TRUNCATED)

    return truncated_references


def calc_sacrebleu(gold_references, model_generations, truncation=False, model_tokenizer=None):
    """
    Calculate SacreBLEU score

    SacreBLEU provides comparable and reproducible BLEU scores.

    :param gold_references: list of target sections
    :param model_generations: list of generated sections
    :param truncation: bool, whether or not to truncate reference sections
    :param model_tokenizer: HuggingFace Tokenizer
    :return: sacrebleu_score
    """

    # truncate the reference sections
    if truncation: gold_references = _truncate_reference_sections(references=gold_references,
                                                                  model_tokenizer=model_tokenizer)
    # check
    assert len(model_generations) == len(gold_references)

    # load the metric
    sacrebleu_metric = datasets.load_metric('sacrebleu')

    # do the preprocessing for calculating sacrebleu - basically make list of lists
    for ind_section in range(len(gold_references)):
        gold_references[ind_section] = [gold_references[ind_section]]

    # check
    assert len(model_generations) == len(gold_references)

    # add reference-generations pairs to metric
    sacrebleu_metric.add_batch(predictions=model_generations, references=gold_references)

    # check
    assert len(sacrebleu_metric) == len(gold_references)

    # computing the metric scores for all samples
    sacrebleu_score = sacrebleu_metric.compute()

    return sacrebleu_score


# Use original bleu
def calc_bleu(gold_references, model_generations, truncation=False, model_tokenizer=None):
    """
    Calculate BLEU score


    :param gold_references: list of target sections
    :param model_generations: list of generated sections
    :param truncation: bool, whether or not to truncate reference sections
    :param model_tokenizer: HuggingFace Tokenizer
    :return: bleu_score
    """

    # truncate the reference sections
    if truncation: gold_references = _truncate_reference_sections(references=gold_references,
                                                                  model_tokenizer=model_tokenizer)

    # check
    assert len(model_generations) == len(gold_references)

    # load the metric
    bleu_metric = datasets.load_metric("bleu")

    # do the preprocessing necessary for calculating bleu

    model_generations = [gen_section.split() for gen_section in model_generations]

    for ind_section in range(len(gold_references)):
        gold_references[ind_section] = [gold_references[ind_section]]

    gold_references = [orig_section[0].split() for orig_section in gold_references]

    for ind_section in range(len(gold_references)):
        gold_references[ind_section] = [gold_references[ind_section]]

    # check
    assert len(model_generations) == len(gold_references)

    # add reference-generations pairs to metric
    bleu_metric.add_batch(predictions=model_generations, references=gold_references)

    # check
    assert len(bleu_metric) == len(gold_references)

    # computing the metric scores for all samples
    bleu_score = bleu_metric.compute()

    return bleu_score


def calc_bertscore(generations, references):

    BERT_scorer = BERTScorer(lang="en", rescale_with_baseline=True)

    precision, recall, F1_score = BERT_scorer.score(generations, references)

    print(f"BERTScore (F1 score): {F1_score.mean():.3f}")

    return F1_score
