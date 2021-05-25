## Data Fetching Steps

RAPID EMA Service provides the RESTful interface to EMA documents.  
(Data as of 12.02.2021)


#### 1. Using RAPID Swagger UI (Bayer tool), return all EMA documents IDs for the type="product-information"
Source: https://ema-docs.dev.rapid.int.bayer.com/swagger-ui.html  
GET method: /EMA/documents/{type} --- Returns all EMA document IDs for the given type

**Input:** type='product-information'  
**Output:** json file with document IDs of type='product-information'

json file is saved as *json/EMA_document_IDs_type_product_information.json*  
(File contains 1660 doc IDs)

#### 2. Script *reformat_json.py* to prepare IDs format for bash script
Remove: 1st line ("[") and last line ("]")
Remove: '\"' and ',' from each line to just have document id and "\n" 

**Output:** json/preprocessed_EMA_document_IDs_type_product_information.json  
(File contains 1660 doc IDs)

#### 3. Bash script to fetch a document given ID (with RAPID API)

Put the bash script *bash-script-get-EMA-docs-rapid.sh* into the folder 'product_information_EMA_documents'  
Run the script from terminal (e.g. git Bash)  

**Output:** Directory contains 1660 documents of type='product-information')   
(Doc IDs are taken from file *json/preprocessed_EMA_document_IDs_type_product_information.json*) 

#### 4. Run create_dataset.py to store leaflets dataset conveniently in one file

Logs:  
Num. of documents processed:  1660    
Total num. of documents failed in extracting full content:  4  
Total num. of documents failed in extracting package leaflet:  2  
Total num. of documents failed in extracting section names:  54  
-------------------- Extracting sections --------------------  
Total num. of documents failed in extracting section 1:  13  
Total num. of documents failed in extracting section 2:  15  
Total num. of documents failed in extracting section 3:  7  
Total num. of documents failed in extracting section 4:  12  
Total num. of documents failed in extracting section 5:  23  
Total num. of documents failed in extracting section 6:  16  


#### 5. Run postprocess_dataset.py to process every section content of each leaflet

**Input**: LEAFLET_DATASET.pickle  
**Output**: LEAFLET_DATASET_PROCESSED.pickle  

Logs:  
Number of documents obtained after running create_dataset.py:  1600   
Number of documents with all sections - None:   0   
Num. of documents with updated section6:  1584   
Number of *unique* leaflets:  1336   
Number of *duplicate* leaflets (by product names):  264    
Number of empty sections (len <= 1):  10    
Number of *duplicate* sections:  144    
COUNT_DUPLICATE_SECTION_1:  1    
COUNT_DUPLICATE_SECTION_2:  0    
COUNT_DUPLICATE_SECTION_3:  0    
COUNT_DUPLICATE_SECTION_4:  13     
COUNT_DUPLICATE_SECTION_5:  130    
COUNT_DUPLICATE_SECTION_6:  0    
Number of *unique* sections:  7787    

#### 6. [Optional] Run test_postprocessing_dataset.py to perform tests of functions in postprocess_dataset.py

Logs:  
Total num. of docs:  1336   
Num. of documents with failed Section6 processing:  0   
Num. of sections with failed URL Removal:  0   
Num. of sections with failed MESSAGE Removal:  0   
Num. of *sections* with failed PAGE_NUMBERS Removal:  19   
Number of duplicate sections marked with a flag:  144   
Number of unique IDs:  1336   
Number of duplicate IDs:  0   
Number of unique URLs:  1336   
Number of duplicate URLs:  0  
Number of unique product names:  1336   
Number of duplicate product names:  0    
Random section[1-6] to display:   
(to exit - press "Enter")  

