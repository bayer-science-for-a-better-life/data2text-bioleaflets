"""
Functionality to process the extracted (raw) data from documents
"""

import pickle
import re
from EMA_documents import SectionLeaflet, Leaflet


def check_none_documents(package_leaflets_raw):
    """
    "None" document - where each section in a document is None

    :param package_leaflets_raw: array of leaflets
    :return: Number of such documents
    """

    COUNT_NONE_DOCUMENTS = 0

    for leaflet in package_leaflets_raw:
        if leaflet.section1 is None and leaflet.section2 is None and leaflet.section3 is None \
                and leaflet.section4 is None and leaflet.section5 is None and leaflet.section6 is None:
            COUNT_NONE_DOCUMENTS += 1
            print("Document --- ", leaflet.id, " has all sections - NONE")

    return COUNT_NONE_DOCUMENTS


def process_section6(package_leaflets_raw):
    """
    In every leaflet's section6 - remove the part after 'Marketing Authorisation Holder' because
    the it contains contact info and addresses (not interesting to generate)

    :param package_leaflets_raw: array of leaflets
    :return: array of leaflets with updated section6 in each leaflet
    """

    NUM_DOC_SECTION6_PROCESSED = 0

    for leaflet in package_leaflets_raw:
        # get the content of section6 from current leaflet
        section6_content = leaflet.section6.section_content

        if section6_content is not None:
            KEYWORDS_1 = ' marketing authorisation holder'
            KEYWORDS_2 = ' marketing authorization holder'

            # if both alternatives of keywords are present - yes, it is possible (for 6 docs)
            if KEYWORDS_1 in section6_content and KEYWORDS_2 in section6_content:
                # which one is earlier
                index_1 = section6_content.find(KEYWORDS_1)
                index_2 = section6_content.find(KEYWORDS_2)
                # split by keywords appearing earlier, keep the 1st part
                if index_1 < index_2:
                    section6_content = section6_content.split(KEYWORDS_1, 1)[0]
                else:
                    section6_content = section6_content.split(KEYWORDS_2, 1)[0]
                # update leaflet
                leaflet.section6.section_content = section6_content
                NUM_DOC_SECTION6_PROCESSED += 1

            # if only one keyword is present in a section
            if len(section6_content.split(KEYWORDS_1, 1)) == 2:
                # keep only the part - everything before KEYWORDS_1
                section6_content = section6_content.split(KEYWORDS_1, 1)[0]
                # update leaflet
                leaflet.section6.section_content = section6_content
                NUM_DOC_SECTION6_PROCESSED += 1

            elif len(section6_content.split(KEYWORDS_2, 1)) == 2:
                # keep only the part - everything before KEYWORDS_2
                section6_content = section6_content.split(KEYWORDS_2, 1)[0]
                # update leaflet
                leaflet.section6.section_content = section6_content
                NUM_DOC_SECTION6_PROCESSED += 1

    # NUM_DOC_SECTION6_PROCESSED = 1584 - makes sense, since None section6 = 16
    print('Num. of documents with updated section6: ', NUM_DOC_SECTION6_PROCESSED)

    return package_leaflets_raw


# Helper Function
def remove_URLs(section_content):
    """
    Remove URL from the section content

    :param section_content: content of a section
    :return: content of a section without URL
    """

    # remove URL with regexp
    section_content = re.sub(r'http\S+', '', section_content)
    section_content = re.sub(r'www\S+', '', section_content)
    section_content = re.sub(r'mailto\S+', '', section_content)

    # remove multiple consecutive spaces
    section_content = re.sub(' +', ' ', section_content)

    return section_content


# Helper Function
def remove_special_message(section_content):
    """
    Remove "medicinal product no longer authorised"

    e.g.
    'me di cin al p ro du ct n o lo ng er a ut ho ris ed'
    'me dic ina l p rod uc t n o l on ge r a uth ori se d'

    :param section_content: content of a section
    :return: content of a section without special message
    """

    # string as it is present in the section content
    SPECIAL_MESSAGE1 = 'me di cin al p ro du ct n o lo ng er a ut ho ris ed'
    SPECIAL_MESSAGE2 = 'me dic ina l p ro du ct no lo ng er au th or ise d'
    SPECIAL_MESSAGE3 = 'me dic ina l p rod uc t n o l on ge r a uth ori se d'
    SPECIAL_MESSAGE4 = 'me dic ina l p ro du ct no lo ng er au tho ris ed'
    SPECIAL_MESSAGE5 = 'me dic ina l p ro du ct no lo ng er a ut ho ris ed'
    SPECIAL_MESSAGE6 = 'me dic ina l p rod uc t n o l on ge r a uth ori sed'
    SPECIAL_MESSAGE7 = 'm ed ici na l p ro du ct no lo ng er a ut ho ris ed'
    SPECIAL_MESSAGE8 = 'm ed ici na l p ro du ct no lo ng er au th or ise d'
    SPECIAL_MESSAGE9 = 'med icin al pro du ct no lo ng er au tho ris ed'
    SPECIAL_MESSAGE_ARRAY = [SPECIAL_MESSAGE1, SPECIAL_MESSAGE2, SPECIAL_MESSAGE3, SPECIAL_MESSAGE4,
                             SPECIAL_MESSAGE5, SPECIAL_MESSAGE6, SPECIAL_MESSAGE7, SPECIAL_MESSAGE8,
                             SPECIAL_MESSAGE9]

    # in case message present in section content
    for SPECIAL_MESSAGE in SPECIAL_MESSAGE_ARRAY:
        section_content = section_content.replace(SPECIAL_MESSAGE, '')

    # remove multiple consecutive spaces
    section_content = re.sub(' +', ' ', section_content)

    return section_content


# Helper Function
def remove_page_numbers(section_content):
    """
    Remove page numbers from section content

    e.g.
    'xeplion.', '69', 'this', 'medicine'
    'several', 'injections.', '49', 'if', 'you'
    'to', 'treat.', '49', 'if', 'you', 'have', 'both'

    pattern page number = '. 41 '

    Note: remove() method will ruin your life, bc it removes the *earliest* element by value
    (instead use - del)
    del - Specify the item to be deleted by index.

    :param section_content: content of a section
    :return: content of a section without page numbers
    """

    # find all 2-digit and 3-digit numbers in section content
    regex = "\d{2,3}"
    numbers_found = re.findall(regex, section_content)

    section_content_tokenized = section_content.split()

    for index, token in enumerate(section_content_tokenized):
        # skip the number if the next token is 'mg'
        if token in numbers_found and (index+1) < len(section_content_tokenized) \
                and section_content_tokenized[index+1] == 'mg':
            continue

        # in case current token is a number and is the 1st token in section content
        if token in numbers_found and index == 0:
            # remove page number at index
            del section_content_tokenized[index]

        # in case current token is a number
        elif token in numbers_found:
            # check whether last character of a previous token is a period
            if section_content_tokenized[index-1][-1] == '.':
                # remove page number - at particular index
                # list remove at index
                del section_content_tokenized[index]

    section_content = " ".join(section_content_tokenized)

    # remove multiple consecutive spaces
    section_content = re.sub(' +', ' ', section_content)

    return section_content


def process_content(section_content):
    # Processing section content

    # skip None sections
    if section_content is None:
        return None

    # remove URLs
    section_content = remove_URLs(section_content)

    # remove "medicinal product no longer authorised" from section content if present
    section_content = remove_special_message(section_content)

    # remove page numbers (following after period)
    section_content = remove_page_numbers(section_content)

    # remove bullet points symbols, e.g. '•'
    section_content = section_content.replace('\uf02d', '')
    section_content = section_content.replace('\uf0b7', '')
    section_content = section_content.replace('\uf0e0', '')
    section_content = section_content.replace('\uf0a7', '')
    section_content = section_content.replace('\uf097', '')
    section_content = section_content.replace('\uf020', '')
    section_content = section_content.replace('\uf06e', '')
    section_content = section_content.replace('\uf076', '')
    section_content = section_content.replace('\uf0e8', '')
    section_content = section_content.replace('\uf0fb', '')
    section_content = section_content.replace('\uf09f', '')
    section_content = section_content.replace('\uf0ee', '')
    section_content = section_content.replace('•', '')
    section_content = section_content.replace('▪', '')
    section_content = section_content.replace('♦', '')
    section_content = section_content.replace('►', '')
    section_content = section_content.replace('➔', '')
    section_content = section_content.replace('■', '')
    section_content = section_content.replace('�', '')
    section_content = section_content.replace('●', '')
    # ord('–') and ord('-') are different chars, one used as bullet point, another - in words
    # remove the one used as a bullet point
    section_content = section_content.replace('–', '')

    # remove special characters
    section_content = section_content.replace('\uf0b0', '')
    section_content = section_content.replace('\uf061', '')
    section_content = section_content.replace('°c', '')
    section_content = section_content.replace('\uf0fc', '')
    section_content = section_content.replace('\uf0ab', '')
    section_content = section_content.replace('\uf0b3', '')

    # process quotes
    section_content = section_content.replace('“', '"')
    section_content = section_content.replace('”', '"')
    section_content = section_content.replace("‘", '\'')
    section_content = section_content.replace("’", '\'')

    # remove multiple consecutive spaces
    section_content = re.sub(' +', ' ', section_content)

    return section_content


def remove_duplicates(package_leaflets):
    """
    Keep only leaflets with unique product_name.

    if each next leaflet, if there is already the leaflet with same product_name - skip the leaflet

    :param package_leaflets: array of processed leaflets
    :return: array of unique leaflets
    """

    # save only leaflets with unique product_name
    package_leaflets_unique = []

    # keep track of unique product names observed so far
    unique_product_names = set()

    COUNT_DUPLICATE_PRODUCT_NAME = 0

    for leaflet in package_leaflets:
        if leaflet.product_name not in unique_product_names:
            unique_product_names.add(leaflet.product_name)
            # save unique leaflet separately
            package_leaflets_unique.append(leaflet)

        # if leaflet.product_name is in unique_product_names - then it is duplicate - do not save
        else:
            COUNT_DUPLICATE_PRODUCT_NAME += 1

    print("Number of *unique* leaflets: ", len(package_leaflets_unique))
    print("Number of *duplicate* leaflets (by product names): ", COUNT_DUPLICATE_PRODUCT_NAME)

    return package_leaflets_unique


def empty_sections(package_leaflets_unique):

    COUNT_SECTIONS_EMPTY = 0

    for leaflet in package_leaflets_unique:
        all_sections_leaflet = [leaflet.section1.section_content, leaflet.section2.section_content,
                                leaflet.section3.section_content, leaflet.section4.section_content,
                                leaflet.section5.section_content, leaflet.section6.section_content]

        for index, section_content in enumerate(all_sections_leaflet):
            if section_content is None:
                continue

            if len(section_content) <= 1:
                COUNT_SECTIONS_EMPTY += 1
                # print(leaflet.id)   # all doc ids - different

    print('Number of empty sections (len <= 1): ', COUNT_SECTIONS_EMPTY)


def check_duplicate_sections(package_leaflets_unique, mark_duplicate_section=True):
    """
    Check the minimum number of duplicate sections
    AND
    if section_content is duplicate in a leaflet - set the field - section.is_duplicate = True

    Minimum because if at least one character is different in 2 section contents
              -> current methods regards these 2 sections - different

    Note: section -> Embeddings -> Better way to check for duplicate section contents

    :param package_leaflets_unique:
    :return:
    """

    COUNT_DUPLICATE_SECTIONS = 0

    COUNT_DUPLICATE_SECTION_1 = 0
    COUNT_DUPLICATE_SECTION_2 = 0
    COUNT_DUPLICATE_SECTION_3 = 0
    COUNT_DUPLICATE_SECTION_4 = 0
    COUNT_DUPLICATE_SECTION_5 = 0
    COUNT_DUPLICATE_SECTION_6 = 0

    unique_sections = set()

    for leaflet in package_leaflets_unique:
        all_sections_leaflet = [leaflet.section1.section_content, leaflet.section2.section_content,
                                leaflet.section3.section_content, leaflet.section4.section_content,
                                leaflet.section5.section_content, leaflet.section6.section_content]

        for index, section_content in enumerate(all_sections_leaflet):
            if section_content is None:
                continue

            # if section_content is already in set - unique_sections, then it is a duplicate
            if section_content in unique_sections and len(section_content) > 1:

                COUNT_DUPLICATE_SECTIONS += 1

                if index == 0:
                    COUNT_DUPLICATE_SECTION_1 += 1
                    # set the "flag" of a duplicate section to True
                    if mark_duplicate_section: leaflet.section1.is_duplicate = True
                    # print(section_content)
                    # print()
                elif index == 1:
                    COUNT_DUPLICATE_SECTION_2 += 1
                    # set the "flag" of a duplicate section to True
                    if mark_duplicate_section: leaflet.section2.is_duplicate = True
                elif index == 2:
                    COUNT_DUPLICATE_SECTION_3 += 1
                    # set the "flag" of a duplicate section to True
                    if mark_duplicate_section: leaflet.section3.is_duplicate = True
                elif index == 3:
                    COUNT_DUPLICATE_SECTION_4 += 1
                    # set the "flag" of a duplicate section to True
                    if mark_duplicate_section: leaflet.section4.is_duplicate = True
                elif index == 4:
                    COUNT_DUPLICATE_SECTION_5 += 1
                    # set the "flag" of a duplicate section to True
                    if mark_duplicate_section: leaflet.section5.is_duplicate = True
                elif index == 5:
                    COUNT_DUPLICATE_SECTION_6 += 1
                    # set the "flag" of a duplicate section to True
                    if mark_duplicate_section: leaflet.section6.is_duplicate = True
            # add section_content to a set
            else:
                unique_sections.add(section_content)

    print('Number of *duplicate* sections: ', COUNT_DUPLICATE_SECTIONS)
    print('COUNT_DUPLICATE_SECTION_1: ', COUNT_DUPLICATE_SECTION_1)
    print('COUNT_DUPLICATE_SECTION_2: ', COUNT_DUPLICATE_SECTION_2)
    print('COUNT_DUPLICATE_SECTION_3: ', COUNT_DUPLICATE_SECTION_3)
    print('COUNT_DUPLICATE_SECTION_4: ', COUNT_DUPLICATE_SECTION_4)
    print('COUNT_DUPLICATE_SECTION_5: ', COUNT_DUPLICATE_SECTION_5)
    print('COUNT_DUPLICATE_SECTION_6: ', COUNT_DUPLICATE_SECTION_6)

    print('Number of *unique* sections: ', len(unique_sections))

    return package_leaflets_unique


if __name__ == '__main__':

    # load array of objects, where object - class Leaflet
    with open("LEAFLET_DATASET.pickle", "rb") as f:
        package_leaflets_raw = pickle.load(f)

    print("Number of documents obtained after running create_dataset.py: ", len(package_leaflets_raw))
    print("Number of documents with all sections - None:  ", check_none_documents(package_leaflets_raw))

    # in section6 remove part after 'marketing authorisation holder'
    package_leaflets = process_section6(package_leaflets_raw)

    # preprocess each section in a leaflet
    for leaflet in package_leaflets:

        # process Section1
        section1_processed = process_content(leaflet.section1.section_content)
        leaflet.section1.section_content = section1_processed

        # process Section2
        section2_processed = process_content(leaflet.section2.section_content)
        leaflet.section2.section_content = section2_processed

        # process Section3
        section3_processed = process_content(leaflet.section3.section_content)
        leaflet.section3.section_content = section3_processed

        # process Section4
        section4_processed = process_content(leaflet.section4.section_content)
        leaflet.section4.section_content = section4_processed

        # process Section5
        section5_processed = process_content(leaflet.section5.section_content)
        leaflet.section5.section_content = section5_processed

        # process Section6
        section6_processed = process_content(leaflet.section6.section_content)
        leaflet.section6.section_content = section6_processed

    # remove duplicate leaflets from dataset
    package_leaflets_unique = remove_duplicates(package_leaflets)

    # find out number of empty sections
    empty_sections(package_leaflets_unique)

    # check the minimum number of duplicate sections
    # set the section.is_duplicate = True if section is duplicate
    package_leaflets_unique = check_duplicate_sections(package_leaflets_unique,
                                                       mark_duplicate_section=True)

    # save processed Leaflets to a file
    with open("LEAFLET_DATASET_PROCESSED.pickle", "wb") as f:
        pickle.dump(package_leaflets_unique, f)
