## Biomedical Data-to-Text Generation via Fine-Tuning Transformers

**Goal**: generate fluent and fact-based descriptions from biomedical data given structured data

![image](https://user-images.githubusercontent.com/14000852/120023051-8dacd280-bfed-11eb-81ae-eeae88c8f79a.png)

### Installation
We used Python 3.7 in our experiments.  

Install latest version from the master branch on Github by:
```
git clone https://github.com/bayer-science-for-a-better-life/data2text-bioleaflets.git
cd data2text-bioleaflets
pip install -r requirements.txt
```






### *BioLeaflets* Dataset

For this purpose we introduce a new biomedical dataset for Data2Text generation - *BioLeaflets*, a corpus of 1336 package leaflets of medicines authorised in Europe, which we obtain by scraping the European Medicines Agency (EMA) [website](https://www.ema.europa.eu/en/glossary/package-leaflet). 
Package leaflets are included in the packaging of medicinal products and contain information to help patients use the product safely and appropriately, under the guidance of their healthcare professional. 
Each document contains six sections: 1) What is the product and what is it used for 2) What you need to know before you take the product 3) product usage instructions 4) possible side effects, 5) product storage conditions 6) other information. 

In our use case we aim to generate package leaflets from structured information about a particular medicine.

![image](https://user-images.githubusercontent.com/14000852/120022403-a7014f00-bfec-11eb-81c9-31325fdc3620.png)


However, there is no structured data available for the package leaflet text. 
Therefore, to create the required input for D2T generation, we augment each document by leveraging named entity recognition (NER) frameworks by [Stanza](https://github.com/stanfordnlp/stanza) and [AWS Comprehend](https://aws.amazon.com/comprehend/).


The newly released dataset could be further used for benchmarking Data2Text generation models in the biomedical domain. 

