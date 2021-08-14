from bert_score import BERTScorer

import datasets
import numpy as np

# MoverScore
from emnlp19_moverscore.moverscore_v2 import get_idf_dict, word_mover_score

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


# Compute original BLEU
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


def calc_rouge(gold_references, model_generations, truncation=False, model_tokenizer=None):
    """
    Calculate ROUGE score

    :param gold_references: list of target sections
    :param model_generations: list of generated sections
    :param truncation: bool, whether or not to truncate reference sections
    :param model_tokenizer: HuggingFace Tokenizer
    :return: rouge_scores
    """

    # truncate the reference sections
    if truncation: gold_references = _truncate_reference_sections(references=gold_references,
                                                                  model_tokenizer=model_tokenizer)

    # check
    assert len(model_generations) == len(gold_references)

    # load the rouge metric
    rouge_metric = datasets.load_metric('rouge')

    # add pairs of predictions/references to a temporary and memory efficient cache table
    rouge_metric.add_batch(predictions=model_generations, references=gold_references)

    # check
    assert len(rouge_metric) == len(model_generations)
    assert len(rouge_metric) == len(gold_references)

    # compute the metric score (after gathering all the cached predictions and references)
    final_score = rouge_metric.compute()

    # computing the metric scores
    rouge_scores = {k: round(v.mid.fmeasure * 100, 4) for k, v in final_score.items()}

    return rouge_scores


def calc_bertscore(generations, references):
    # TODO - implementation with original bertscore (no huggingface)

    BERT_scorer = BERTScorer(lang="en", rescale_with_baseline=True)

    precision, recall, F1_score = BERT_scorer.score(generations, references)

    print(f"BERTScore (F1 score): {F1_score.mean():.3f}")

    return F1_score


def calc_bertscore_hf(gold_references, model_generations):
    """
    Calculate BERTScore with HuggingFace API

    :param gold_references: list of target sections
    :param model_generations: list of generated sections
    :return: bertscore: mean of F1-scores for all references - generations sections
    """

    # check
    assert len(model_generations) == len(gold_references)

    # load the metric
    bertscore_metric = datasets.load_metric('bertscore')

    # computer the bertscore
    bertscore = bertscore_metric.compute(predictions=model_generations, references=gold_references,
                                         lang="en", rescale_with_baseline=True)

    # report the mean of F1-scores of all samples
    final_bertscore = np.mean(bertscore['f1'])

    print('\n BERTScore calculated with ', bertscore['hashcode'])
    print('BERTScore Result:', final_bertscore, '\n')

    return final_bertscore


def calc_moverscore(gold_references, model_generations, n_gram=2, batch_size=16):
    """
    Calculate MoverScore

    :param gold_references: list of target sections
    :param model_generations: list of generated sections
    :param n_gram: unigram-based MoverScore (n-gram=1), bigram-based MoverScore (n-gram=2)
    :param batch_size: size of a batch
    :return: mover_score
    """

    # check
    assert len(model_generations) == len(gold_references)

    idf_dict_hyp = get_idf_dict(model_generations)
    idf_dict_ref = get_idf_dict(gold_references)

    mover_scores = word_mover_score(refs=gold_references, hyps=model_generations, idf_dict_ref=idf_dict_ref,
                                    idf_dict_hyp=idf_dict_hyp, stop_words=[], n_gram=n_gram, remove_subwords=True,
                                    batch_size=batch_size)

    return np.mean(mover_scores)
