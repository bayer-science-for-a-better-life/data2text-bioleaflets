"""
Functionality to process the extracted (raw) data from documents
"""

import pickle
import re
import random
from EMA_documents import SectionLeaflet, Leaflet


def test_process_section6(package_leaflets_processed):

    COUNT_DOCS_SECTION6_NOT_PROC = 0

    for leaflet in package_leaflets_processed:
        KEYWORDS_1 = 'marketing authorisation holder'
        KEYWORDS_2 = 'marketing authorization holder'

        if leaflet.section6.section_content is None:
            continue

        if KEYWORDS_1 in leaflet.section6.section_content or \
                KEYWORDS_2 in leaflet.section6.section_content:
            COUNT_DOCS_SECTION6_NOT_PROC += 1
            print(leaflet.id, " -------------- ", "Section6 NOT processed!")
            print(leaflet.section6.section_content)

    print("Num. of documents with failed Section6 processing: ", COUNT_DOCS_SECTION6_NOT_PROC)

    return 0


def test_remove_URLs(package_leaflets_processed):

    COUNT_SECTIONS_URL_NOT_REMOVED = 0

    for leaflet in package_leaflets_processed:
        all_sections_leaflet = [leaflet.section1.section_content, leaflet.section2.section_content,
                                leaflet.section3.section_content, leaflet.section4.section_content,
                                leaflet.section5.section_content, leaflet.section6.section_content]

        for section_content in all_sections_leaflet:
            if section_content is None:
                continue

            # try to remove URL again
            new_content = re.sub(r'http\S+', '', section_content)

            # if succeed in removing URL - notify
            if len(new_content) != len(section_content):
                COUNT_SECTIONS_URL_NOT_REMOVED += 1
                print(leaflet.id, " -------------- ", "URL NOT removed!")
                print(section_content)

            # just check for URLs
            if 'www.' in section_content or 'http' in section_content or 'mailto' in section_content:
                COUNT_SECTIONS_URL_NOT_REMOVED += 1
                print(leaflet.id, " -------------- ", "URL NOT removed!")
                print(section_content)

    print("Num. of sections with failed URL Removal: ", COUNT_SECTIONS_URL_NOT_REMOVED)


def test_remove_special_message(package_leaflets_processed):

    COUNT_SECTIONS_MESSAGE_NOT_REMOVED = 0

    for leaflet in package_leaflets_processed:
        all_sections_leaflet = [leaflet.section1.section_content, leaflet.section2.section_content,
                                leaflet.section3.section_content, leaflet.section4.section_content,
                                leaflet.section5.section_content, leaflet.section6.section_content]

        for section_content in all_sections_leaflet:
            if section_content is None:
                continue

            # for SPECIAL_MESSAGE in SPECIAL_MESSAGE_ARRAY:
            section_content_tokenized = section_content.split()

            # try to find common token 'me' (part of message) in section content
            if 'me' in section_content_tokenized:
                print(leaflet.id, " -------------- ", "MESSAGE NOT removed!")
                print(section_content)
                COUNT_SECTIONS_MESSAGE_NOT_REMOVED += 1

            if 'medicinal product no longer authorised' in section_content_tokenized:
                print(leaflet.id, " -------------- ", "MESSAGE NOT removed!")
                print(section_content)
                COUNT_SECTIONS_MESSAGE_NOT_REMOVED += 1

    print("Num. of sections with failed MESSAGE Removal: ", COUNT_SECTIONS_MESSAGE_NOT_REMOVED)


def test_remove_page_numbers(package_leaflets_processed):

    COUNT_SECTIONS_PAGENUMBERS_NOT_REMOVED = 0

    for leaflet in package_leaflets_processed:
        all_sections_leaflet = [leaflet.section1.section_content, leaflet.section2.section_content,
                                leaflet.section3.section_content, leaflet.section4.section_content,
                                leaflet.section5.section_content, leaflet.section6.section_content]

        for section_content in all_sections_leaflet:
            if section_content is None:
                continue

            section_content_tokenized = section_content.split()

            flag = 0

            for index, token in enumerate(section_content_tokenized):
                if token.isdigit() and len(token) >= 2:
                    if section_content_tokenized[index-1][-1] == ".":
                        if (index+1) < len(section_content_tokenized) and \
                                section_content_tokenized[index+1] != 'mg':
                            flag = 1
                            # print(leaflet.id, " -------------- ", "PAGE_NUMBERS NOT REMOVED!")
                            # print(section_content)
                            # print(numbers_found)
            if flag == 1:
                COUNT_SECTIONS_PAGENUMBERS_NOT_REMOVED += 1

    print("Num. of *sections* with failed PAGE_NUMBERS Removal: ", COUNT_SECTIONS_PAGENUMBERS_NOT_REMOVED)


def test_duplicate_sections(package_leaflets_processed):

    # should be 144
    COUNT_DUPLICATE_SECTIONS = 0

    unique_sections = set()

    for leaflet in package_leaflets_processed:
        all_sections_leaflet = [leaflet.section1.section_content, leaflet.section2.section_content,
                                leaflet.section3.section_content, leaflet.section4.section_content,
                                leaflet.section5.section_content, leaflet.section6.section_content]

        for index, section_content in enumerate(all_sections_leaflet):
            if section_content is None:
                continue

            # if section_content is already in set - unique_sections, then it is a duplicate
            if section_content in unique_sections and len(section_content) > 1:

                if index == 0:
                    if leaflet.section1.is_duplicate == True: COUNT_DUPLICATE_SECTIONS += 1
                elif index == 1:
                    if leaflet.section2.is_duplicate == True: COUNT_DUPLICATE_SECTIONS += 1
                elif index == 2:
                    if leaflet.section3.is_duplicate == True: COUNT_DUPLICATE_SECTIONS += 1
                elif index == 3:
                    if leaflet.section4.is_duplicate == True: COUNT_DUPLICATE_SECTIONS += 1
                elif index == 4:
                    if leaflet.section5.is_duplicate == True: COUNT_DUPLICATE_SECTIONS += 1
                elif index == 5:
                    if leaflet.section6.is_duplicate == True: COUNT_DUPLICATE_SECTIONS += 1

            # add section_content to a set
            else:
                unique_sections.add(section_content)

    print("Number of duplicate sections marked with a flag: ", COUNT_DUPLICATE_SECTIONS)

    # from postprocess.py - should be 144
    assert COUNT_DUPLICATE_SECTIONS == 144, "In postprocess.check_duplicate_sections - " \
                                            "Not all duplicate sections marked as so"


def test_remove_duplicates(package_leaflets_processed):

    # check whether there are duplicate leaflets
    # find duplicate product ids
    COUNT_DUPLICATE_IDs = 0
    duplicate_ids = []

    unique_ids = set()

    for leaflet in package_leaflets_processed:
        if leaflet.id in unique_ids:
            duplicate_ids.append(leaflet.id)
            COUNT_DUPLICATE_IDs += 1
        else:
            unique_ids.add(leaflet.id)

    print("Number of unique IDs: ", len(unique_ids))
    print("Number of duplicate IDs: ", COUNT_DUPLICATE_IDs)

    # find duplicate product URLs
    COUNT_DUPLICATE_URLs = 0
    duplicate_URLs = []

    unique_URLs = set()

    for leaflet in package_leaflets_processed:
        if leaflet.url in unique_URLs:
            duplicate_URLs.append(leaflet.url)
            COUNT_DUPLICATE_URLs += 1
        else:
            unique_URLs.add(leaflet.url)

    print("Number of unique URLs: ", len(unique_URLs))
    print("Number of duplicate URLs: ", COUNT_DUPLICATE_URLs)

    # find duplicate product names
    COUNT_DUPLICATE_PRODUCT_NAMES = 0
    duplicate_product_names = []

    unique_product_names = set()

    for leaflet in package_leaflets_processed:
        if leaflet.product_name in unique_product_names:
            duplicate_product_names.append(leaflet.product_name)
            COUNT_DUPLICATE_PRODUCT_NAMES += 1
        else:
            unique_product_names.add(leaflet.product_name)

    print("Number of unique product names: ", len(unique_product_names))
    print("Number of duplicate product names: ", COUNT_DUPLICATE_PRODUCT_NAMES)
    # print("Duplicate product names: ", duplicate_product_names)

    return duplicate_product_names, duplicate_URLs


def show_random_section(package_leaflets_processed):

    section_num = '1'

    while section_num:
        section_num = input('Random section[1-6] to display: ')

        if len(section_num) == 0:
            break

        if section_num not in ['1', '2', '3', '4', '5', '6']:
            section_num = '1'

        random_leaflet_index = random.randint(0, len(package_leaflets_processed)-1)

        random_leaflet = package_leaflets_processed[random_leaflet_index]

        all_sections_leaflet = [random_leaflet.section1.section_content, random_leaflet.section2.section_content,
                                random_leaflet.section3.section_content, random_leaflet.section4.section_content,
                                random_leaflet.section5.section_content, random_leaflet.section6.section_content]

        for index in range(len(all_sections_leaflet)):
            if index == int(section_num)-1:
                print(all_sections_leaflet[index])


if __name__ == '__main__':

    # load array of objects, where object - class Leaflet
    with open("bioleaflets_preparation/LEAFLET_DATASET_PROCESSED.pickle", "rb") as f:
        package_leaflets_processed = pickle.load(f)

    print('Total num. of docs: ', len(package_leaflets_processed))

    # test processing section6 function
    test_process_section6(package_leaflets_processed)

    # test removing URLs in each section
    test_remove_URLs(package_leaflets_processed)

    # test removing special message each section
    test_remove_special_message(package_leaflets_processed)

    # test removing special message each section
    test_remove_page_numbers(package_leaflets_processed)

    # test duplicate sections
    test_duplicate_sections(package_leaflets_processed)

    # test for duplicate leaflets
    test_remove_duplicates(package_leaflets_processed)

    # manually examine sections
    show_random_section(package_leaflets_processed)
