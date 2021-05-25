
"""
Preprocess the format of the file "json/EMA_document_IDs_type_product_information.json"
to be suitable for bash script (fetch documents by document ID)

:output: new file "json/preprocessed_EMA_document_IDs_type_product_information.json"
"""

# open file to save the processed data
output_file = open("json/preprocessed_EMA_document_IDs_type_product_information.json", "w")

# count number of doc ids
NUM_DOC_IDS = 0

with open("json/EMA_document_IDs_type_product_information.json") as file:

    # read the content of a file
    file_content = file.readlines()

    # re-format each document ID in a file
    for line in file_content:

        # keep track of number of document IDs
        NUM_DOC_IDS += 1

        # pre-process doc ids by removing '"' and ','
        line = line.replace('"', '')
        line = line.replace(',', '')

        # write to output file
        output_file.write(line)

# close the output file
output_file.close()

# check to re-format all IDs
print("Total number of doc ids: {}".format(NUM_DOC_IDS))
