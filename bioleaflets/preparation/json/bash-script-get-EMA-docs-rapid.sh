#!/bin/bash

# file contains all the doc ids
ALL_DOCS_FILE='preprocessed_EMA_document_IDs_type_product_information.json'

# 1st part of url construction for curl command
URL_PART1="http://<Bayer-ID-placeholder>:<password-placeholder>@svc-proxy.bayerbbs.net:8080 https://ema-docs.dev.rapid.int.bayer.com/EMA/document/"

while read line; do
# reading each line - doc id


# remove the last character "\n" from the line
new_line=${line%?}

# create the url with the doc id
URL="$URL_PART1$new_line"


# calling curl with the doc id
# save output to the file
curl --proxy $URL > ${new_line}.json

done < $ALL_DOCS_FILE
