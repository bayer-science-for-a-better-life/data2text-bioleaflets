## Biomedical Data-to-Text Generation via Fine-Tuning Transformers

**Goal**: generate fluent and fact-based descriptions from biomedical data given structured data

![image](https://user-images.githubusercontent.com/14000852/120023051-8dacd280-bfed-11eb-81ae-eeae88c8f79a.png)

We show that fine-tuned transformers are able to generate realistic, multisentence text from data in the biomedical domain, yet have important limitations.  

### *BioLeaflets* Dataset

For this purpose we introduce a new biomedical dataset for Data2Text generation - *BioLeaflets*, a corpus of 1336 package leaflets of medicines authorised in Europe, which we obtain by scraping the European Medicines Agency (EMA) [website](https://www.ema.europa.eu/en/glossary/package-leaflet). 
Package leaflets are included in the packaging of medicinal products and contain information to help patients use the product safely and appropriately, under the guidance of their healthcare professional. 
Each document contains six sections: 1) What is the product and what is it used for 2) What you need to know before you take the product 3) product usage instructions 4) possible side effects, 5) product storage conditions 6) other information. 

In our use case we aim to generate package leaflets from structured information about a particular medicine.

![image](https://user-images.githubusercontent.com/14000852/120022403-a7014f00-bfec-11eb-81c9-31325fdc3620.png)


However, there is no structured data available for the package leaflet text. 
Therefore, to create the required input for D2T generation, we augment each document by leveraging named entity recognition (NER) frameworks by [Stanza](https://github.com/stanfordnlp/stanza) and [AWS Comprehend](https://aws.amazon.com/comprehend/).  

The newly released dataset could be further used for benchmarking Data2Text generation models in the biomedical domain. 

### Methods

We present baseline results on *BioLeaflets* dataset by fine-tuning the following state-of-the-art language models in seq2seq setting:   
- T5: a text-to-text transfer transformer model ([Raffel et al., 2020](https://arxiv.org/pdf/1910.10683.pdf)).  
- BART: denoising autoencoder for pretraining sequence-to-sequence models with transformers ([Lewis et al., 2020](https://arxiv.org/pdf/1910.13461.pdf)).  


### Installation
We used Python 3.7 in our experiments.  

Install latest version from the master branch on Github by:
```
git clone <GITHUB-URL>
cd data2text-bioleaflets
pip install -r requirements.txt
```

### Data for Fine-Tuning

If you are using your own data, it must be formatted as one directory with 6 files:   
```
train.source
train.target
val.source
val.target
test.source
test.target
```

The `.source` files are the input, the `.target` files are the desired output.   

We prepared *BioLeaflets* dataset in such format and saved at `scripts/data/`.

### Fine-Tuning

Use the `finetune_trainer.py` script for fine-tuning T5 and BART models in seq2seq fashion. The script adapted from [HuggingFace transformers library](https://github.com/huggingface/transformers).   

To see all the possible command line options, run:   
`python finetune_trainer.py --help`


To fine-tune the pre-trained models and reproduce our results in the paper, invoke the training script in the following way:   

```
# indicate path to input dir
export DATA_DIR="~/data2text-bioleaflets/scripts/data/plain"

# indicate path to output dir
export DATA_DIR_OUT="~/data2text-bioleaflets/results/T5_plain"
```

```
python scripts/finetune_trainer.py \
--model_name_or_path t5-base \
--data_dir $DATA_DIR \
--output_dir $DATA_DIR_OUT \
--n_train -1 \
--n_val -1 \
--n_test -1 \
--max_target_length 512 \
--val_max_target_length 512 \
--test_max_target_length 512 \
--task summarization \
--save_steps 2000 \
--num_train_epochs 20 \
--save_total_limit 4 \
--do_train True \
--do_eval False \
--do_predict False \
--predict_with_generate False \
--evaluation_strategy no \
--gradient_accumulation_steps 16 \
--per_device_train_batch_size 2 \
--per_device_eval_batch_size 8 \
--learning_rate 1e-3 \
--seed 1
```

### Generations and Evaluations
To create target sections for each set of corresponding Entities in *BioLeaflets* dataset, we use `run_eval.py`. 
The computed metric is ROUGE be default.   

Predictions for test data:     
```
python scripts/run_eval.py \
$DATA_DIR_OUT \
$DATA_DIR/test.source \
$DATA_DIR_OUT/test_generations_beam_1.txt \
--reference_path $DATA_DIR/test.target \
--score_path $DATA_DIR_OUT/test_scores_beam_1.json \
--device cuda \
--bs 16 \
--num_beams 1
```




### Generation examples

Generations of *BioLeaflets* test dataset with different models you can find in `results/` directory.  

![image](https://user-images.githubusercontent.com/14000852/120937066-a747cb80-c70b-11eb-8155-2b3c72a69326.png)
