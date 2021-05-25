"""
Structure the package leaflets in a convenient and compact form

Store information as an array of objects, where each object - Package Leaflet of 1 product(drug)

"""

import json
import pickle
import os
import logging

from EMA_documents import SectionLeaflet, Leaflet
import parse_json


# set up logging
logging.basicConfig(filename='create_dataset.log', filemode='w', level=logging.INFO)

# count the number of docs processed (should be 1660)
NUM_DOC_PROCESSED = 0

# count the number of docs for which extracting basic info - failed
NUM_DOC_FAILED_FULL_CONTENT = 0

# count the number of docs for which extracting package leaflet - failed
NUM_DOC_FAILED_LEAFLET = 0

# count number of times extracting section names failed
SECTION_NAMES_FAILED = 0

# count number of times extracting section{1-6} failed
SECTION_1_FAILED = 0
SECTION_2_FAILED = 0
SECTION_3_FAILED = 0
SECTION_4_FAILED = 0
SECTION_5_FAILED = 0
SECTION_6_FAILED = 0

# array to store all the leaflets
package_leaflets = []

# for each EMA file of the type - product information
for filename in os.listdir('json/product_information_EMA_documents/'):

    # path to the particular file
    path2file = 'json/product_information_EMA_documents/' + filename

    # load the data of the document
    with open(path2file, encoding='utf-8') as json_file:
        file_data = json.load(json_file)

    NUM_DOC_PROCESSED += 1

    # get the basic info about the product from document
    product_name, product_url, product_id, product_content \
        = parse_json.extract_doc_info(file_data)

    # if no product content in document - skip the document
    if product_content is None:
        print(filename, " ---- No product content found in the document")
        NUM_DOC_FAILED_FULL_CONTENT += 1
        continue

    # extract package leaflet part from the document
    package_leaflet = parse_json.extract_package_leaflet(product_content, product_id)

    # if no package leaflet in document - skip the document
    if package_leaflet is None:
        print(filename, " ---- No leaflet found in the document")
        NUM_DOC_FAILED_LEAFLET += 1
        continue

    # extract section names from package leaflet and leaflet without table_of_content info
    section_names, leaflet = \
        parse_json.extract_section_names(package_leaflet, product_id)

    # if failed extracting section names and leaflet without toc - skip the document
    if section_names is None or leaflet is None:
        print(filename, " ---- No section names found in the document")
        SECTION_NAMES_FAILED += 1
        continue

    # extract sections

    section1_content = parse_json.extract_section1(section_names, leaflet, product_name)
    if section1_content is None:
        print(filename, " ---- Section 1 Extraction Failed in the document")
        SECTION_1_FAILED += 1

    section2_content = parse_json.extract_section2(section_names, leaflet, product_name)
    if section2_content is None:
        print(filename, " ---- Section 2 Extraction Failed in the document")
        SECTION_2_FAILED += 1

    section3_content = parse_json.extract_section3(section_names, leaflet, product_name)
    if section3_content is None:
        print(filename, " ---- Section 3 Extraction Failed in the document")
        SECTION_3_FAILED += 1

    section4_content = parse_json.extract_section4(section_names, leaflet, product_name)
    if section4_content is None:
        print(filename, " ---- Section 4 Extraction Failed in the document")
        SECTION_4_FAILED += 1

    section5_content = parse_json.extract_section5(section_names, leaflet, product_name)
    if section5_content is None:
        print(filename, " ---- Section 5 Extraction Failed in the document")
        SECTION_5_FAILED += 1

    section6_content = parse_json.extract_section6(section_names, leaflet, product_name)
    if section6_content is None:
        print(filename, " ---- Section 6 Extraction Failed in the document")
        SECTION_6_FAILED += 1

    # create SectionLeaflet objects

    section1 = SectionLeaflet(title=section_names['1'],
                              section_content=section1_content,
                              entity_recognition=None)

    section2 = SectionLeaflet(title=section_names['2'],
                              section_content=section2_content,
                              entity_recognition=None)

    section3 = SectionLeaflet(title=section_names['3'],
                              section_content=section3_content,
                              entity_recognition=None)

    section4 = SectionLeaflet(title=section_names['4'],
                              section_content=section4_content,
                              entity_recognition=None)

    section5 = SectionLeaflet(title=section_names['5'],
                              section_content=section5_content,
                              entity_recognition=None)

    section6 = SectionLeaflet(title=section_names['6'],
                              section_content=section6_content,
                              entity_recognition=None)

    # create Leaflet object for current document

    current_leaflet = Leaflet(product_name=product_name,
                              product_url=product_url,
                              product_id=product_id,
                              product_content=product_content,
                              section1=section1,
                              section2=section2,
                              section3=section3,
                              section4=section4,
                              section5=section5,
                              section6=section6)

    package_leaflets.append(current_leaflet)

# save array with Leaflet objects to a file
with open("LEAFLET_DATASET.pickle", "wb") as f:
    pickle.dump(package_leaflets, f)

# print information

print("Num. of documents processed: ", NUM_DOC_PROCESSED)
print("Total num. of documents failed in extracting full content: ", NUM_DOC_FAILED_FULL_CONTENT)
print("Total num. of documents failed in extracting package leaflet: ", NUM_DOC_FAILED_LEAFLET)
print("Total num. of documents failed in extracting section names: ", SECTION_NAMES_FAILED)

print("-------------------- Extracting sections --------------------")

print("Total num. of documents failed in extracting section 1: ", SECTION_1_FAILED)
print("Total num. of documents failed in extracting section 2: ", SECTION_2_FAILED)
print("Total num. of documents failed in extracting section 3: ", SECTION_3_FAILED)
print("Total num. of documents failed in extracting section 4: ", SECTION_4_FAILED)
print("Total num. of documents failed in extracting section 5: ", SECTION_5_FAILED)
print("Total num. of documents failed in extracting section 6: ", SECTION_6_FAILED)

