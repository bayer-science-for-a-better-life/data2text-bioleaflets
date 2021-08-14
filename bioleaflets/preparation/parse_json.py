"""
Structure the package leaflets in a convenient and compact form

Store information as an array of objects, where each object - Package Leaflet of 1 product(drug)
"""

import logging


# helper function
def process_string(string):
    """
    # strip() method removes whitespace, \n, \t at the beginning and end (both sides) of a string

    :param string: any string
    :return: processed string
    """

    string = string.strip()
    string = string.strip('\n')
    string = string.strip('\t')
    string = string.strip()

    return string


def extract_doc_info(file_data):
    """
    Extract all the basic information about the product from a document

    :param file_data
    :return: product_name, product_url, product_id, product_content
    """

    # get id
    try:
        product_id = file_data['attachment'][0]['id']
    except:
        logging.info('[Basic Info Extraction] - Can not get the id')
        product_id = None

    # get product name
    try:
        product_name = file_data["product_name"]
    except:
        logging.info('[Basic Info Extraction] - Can not get the product name. Doc id: %s', product_id)
        product_name = None

    # preprocess product name - in case there is old name of a product - remove
    if product_name is not None and '(previously' in product_name.split():
        product_name_tokenized = product_name.split()
        index = product_name_tokenized.index('(previously')

        # keep the newest product name
        product_name = " ".join(product_name_tokenized[:index])

    # get url
    try:
        product_url = file_data["attachment"][0]['link']
    except:
        logging.info('[Basic Info Extraction] - Can not get the product url. Doc id: %s', product_id)
        product_url = None

    # get full content
    try:
        product_content = file_data['attachment'][0]['content']
    except:
        logging.warning('[Basic Info Extraction] - Can not get the product content. Doc id: %s', product_id)
        product_content = None

    return product_name, product_url, product_id, product_content


def extract_package_leaflet(doc_content, product_id):
    """
    Given the full document content extract PACKAGE LEAFLET part

    :param doc_content: full content of the document
    :param product_id: ID of the product (document)
    :return: leaflet or None
    """

    # Tokenize content by a whitespace
    doc_content_tokenized = doc_content.split()

    # Join everything together
    doc_content = " ".join(doc_content_tokenized)

    # Get the Leaflet part of the document

    # Select everything after the starting phrase of a leaflet
    PACKAGE_LEAFLET_NAME_1 = 'B. PACKAGE LEAFLET'
    PACKAGE_LEAFLET_NAME_2 = 'B.PACKAGE LEAFLET'
    PACKAGE_LEAFLET_NAME_3 = 'PACKAGE LEAFLET'

    try:
        leaflet = doc_content.split(PACKAGE_LEAFLET_NAME_1, 1)[1]
    except:
        # print('[Leaflet Extraction] Error - Extracting Leaflet Part1: ', product_id)
        logging.warning('[Leaflet Extraction] Error - Extracting Leaflet Part1: %s', product_id)

        try:
            leaflet = doc_content.split(PACKAGE_LEAFLET_NAME_2, 1)[1]
            logging.warning('[Leaflet Extraction] SUCCESS - Extracting Leaflet Part2: %s', product_id)
        except:
            # print('[Leaflet Extraction] Error - Extracting Leaflet Part2: ', product_id)
            logging.warning('[Leaflet Extraction] Error - Extracting Leaflet Part2: %s', product_id)

            try:
                leaflet = doc_content.split(PACKAGE_LEAFLET_NAME_3, 1)[1]
                logging.warning('[Leaflet Extraction] SUCCESS - Extracting Leaflet Part3: %s', product_id)
            except:
                # print('[Leaflet Extraction] Error - Extracting Leaflet Part3: ', product_id)
                logging.warning('[Leaflet Extraction] Error - Extracting Leaflet Part3: %s', product_id)
                # give up extracting leaflet after 3 attempts
                leaflet = None

    if leaflet is None:
        return None

    # Select everything before the ending phrase of a leaflet
    LEAFLET_END = 'This leaflet was last revised in'
    try:
        leaflet = leaflet.split(LEAFLET_END, 1)[0]
    except:
        # print('[Leaflet Extraction] Error - Extracting LEAFLET_END: ', product_id)
        logging.warning('[Leaflet Extraction] Error - Extracting LEAFLET_END: %s', product_id)
        return None

    return leaflet


def extract_section_names(package_leaflet, product_id):
    """
    Extract section names from table_of_content (ToC) and extract leaflet without ToC

    :param package_leaflet: Content of package leaflet
    :param product_id: Id of the current package leaflet

    :return: section_names, leaflet_without_ToC
    """

    # lowercase content of package leaflet
    package_leaflet = package_leaflet.lower()

    # extract everything after ToC
    TABLE_OF_CONTENT = 'what is in this leaflet 1.'

    try:
        package_leaflet = package_leaflet.split(TABLE_OF_CONTENT, 1)[1]
    except:

        try:
            TABLE_OF_CONTENT = 'in this leaflet: 1.'
            package_leaflet = package_leaflet.split(TABLE_OF_CONTENT, 1)[1]
        except:

            try:
                TABLE_OF_CONTENT = 'in this leaflet 1.'
                package_leaflet = package_leaflet.split(TABLE_OF_CONTENT, 1)[1]
            except:
                logging.warning('[TOC] Error - Extracting TOC: %s', product_id)
                # give up
                return None, None

    # extract the section1 title from ToC
    START_SECTION2 = '2.'

    section1_title = package_leaflet.split(START_SECTION2, 1)[0]

    # hard-coded removal of not-standard ("noisy") documents
    if len(section1_title) >= 100:
        # give up (skipped around 2 docs)
        return None, None

    section1_title = process_string(section1_title)

    # extract leaflet without table of content (ToC)
    try:
        leaflet_without_toc = package_leaflet.split(section1_title, 2)[2]
    except:
        # print('[TOC] Error - Extracting Leaflet without TOC: ', product_id)
        logging.warning('[TOC] Error - Extracting Leaflet without TOC: %s', product_id)
        return None, None

    # add back section1_title to leaflet without ToC
    leaflet_without_toc = '1. ' + section1_title + leaflet_without_toc

    # extract only table of content from leaflet - technically ToC without section1_title
    try:
        table_of_content = package_leaflet.split(section1_title, 2)[1]
    except:
        print('[TOC] Error - Extracting <only> TOC: ', product_id)
        return None, None

    # hard-coded removal of non-standard ("noisy") documents
    if len(table_of_content) > 800:
        return None, None

    # preprocess table of content
    table_of_content = process_string(table_of_content)

    # table_of_content = '2. what you need to know before you use trydonis
    # 3. how to use trydonis 4. possible side effects 5. how to store trydonis
    # 6. contents of the pack and other information 1.'

    # Section 1 title
    section1_title = '1. ' + section1_title

    # Section 2 title
    section2_title = table_of_content.split('3.')[0]
    section2_title = process_string(section2_title)

    # Section 3 title
    start_section3 = table_of_content.find('3')
    end_section3 = table_of_content.find('4')
    section3_title = table_of_content[start_section3:end_section3]
    section3_title = process_string(section3_title)

    # Section 4 title
    start_section4 = table_of_content.find('4')
    end_section4 = table_of_content.find('5')
    section4_title = table_of_content[start_section4:end_section4]
    section4_title = process_string(section4_title)

    # Section 5 title
    start_section5 = table_of_content.find('5')
    end_section5 = table_of_content.find('6')
    section5_title = table_of_content[start_section5:end_section5]
    section5_title = process_string(section5_title)

    # Section 6 title - Tricky - because section 7 might exist
    start_section6 = table_of_content.find('6')

    if table_of_content.find('7') == -1:
        end_section6 = table_of_content.find('1')
    else:
        end_section6 = table_of_content.find('7')

    section6_title = table_of_content[start_section6:end_section6]
    section6_title = process_string(section6_title)

    # use dictionary instead of array - not to mess up the order of sections
    output_sections = dict()
    output_sections['1'] = section1_title
    output_sections['2'] = section2_title
    output_sections['3'] = section3_title
    output_sections['4'] = section4_title
    output_sections['5'] = section5_title
    output_sections['6'] = section6_title

    return output_sections, leaflet_without_toc


def extract_section1(section_names, leaflet, product_name):
    """
    Extract Section1 from the leaflet_without_ToC (table of content)

    Explanation:
    - standard (input) leaflet structure - section1_title, content_section1, section2_title, content_section2 ...
    - splitting leaflet by e.g. section1_title *has to result in* 2 parts - everything before section1_title,
    everything after section1_title; these parts correspond to 2 arrays
    - so first split leaflet by section1_title and select (2nd part) - section1_content, section2_title, section2_content
    - then split (2nd part) by section2_title and select 1st part - just section1_content
    - Repeat same approach for all other sections!

    *Assumption*: splitting by section{N}_title has always result in 2 parts - everything before section{N}_title,
    everything after section{N}_title. If that's not the case --- smth is wrong with the structure of the leaflet,
    or there are spelling mistakes (e.g. typos in section{N}_title)


    :param section_names: section titles of the package leaflet
    :param leaflet: package leaflet without the table of content
    :param product_name: name of the product
    :return: section1 content
    """

    section1_title = section_names['1']
    section2_title = section_names['2']

    # hard-coded alternatives to section2_title based on personal observations
    alternative_1 = '2. what you need to know before you are given {}'.format(product_name.lower())
    alternative_2 = '2. what you need to know before you take {}'.format(product_name.lower())
    alternative_3 = '2. what you need to know before you use {}'.format(product_name.lower())
    alternative_4 = '2 what you need to know before you take {}'.format(product_name.lower())
    alternative_5 = '2. what do you need to know before you take {}'.format(product_name.lower())

    alternative_section2_title = [alternative_1, alternative_2, alternative_3, alternative_4, alternative_5]

    # section1 content in between section1_title and section2_title
    try:
        section1_content = leaflet.split(section1_title, 1)[1]

        # make sure splitting by section1_title worked properly - validate assumption in docstring
        assert len(leaflet.split(section1_title, 1)[0]) == 0, "There is text before the section1 title"
        assert len(leaflet.split(section1_title, 1)) == 2, "There are multiple section1_title in leaflet_without_ToC, " \
                                                           "has to be only 1 section1_title"
    except:
        return None

    try:
        # Case when section2_title from ToC matches section2_title in leaflet
        if len(section1_content.split(section2_title, 1)) == 2:
            section1_content = section1_content.split(section2_title, 1)[0]

        elif len(section1_content.split(section2_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section2_title from ToC

            flag = 0
            for alternative in alternative_section2_title:
                # check if alternative matches the section2_title in leaflet
                if len(section1_content.split(alternative, 1)) == 2:
                    flag = 1
                    section1_content = section1_content.split(alternative, 1)[0]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # remove whitespaces in the beginning/end of string
    section1_content = process_string(section1_content)

    return section1_content


def extract_section2(section_names, leaflet, product_name):
    """
    Extract Section2 from the leaflet_without_ToC (without table of content)

    Explanation:
    - standard (input) leaflet structure - section1_title, content_section1, section2_title, content_section2 ...
    - splitting leaflet by e.g. section1_title *has to result in* 2 parts - everything before section1_title,
    everything after section1_title; these parts correspond to 2 arrays
    - so first split leaflet by section1_title and select (2nd part) - section1_content, section2_title, section2_content
    - then split (2nd part) by section2_title and select 1st part - just section1_content
    - Repeat same approach for all other sections!

    *Assumption*: splitting by sectionN_title has always result in 2 parts - everything before sectionN_title,
    everything after sectionN_Title. If that's not the case --- smth is wrong with the structure of the leaflet,
    or there are spelling mistakes, typos in sectionN_title


    :param section_names: section titles of the package leaflet
    :param leaflet: package leaflet without the table of content
    :param product_name: name of the product
    :return: section2 content
    """

    # section titles from Table of Content
    section2_title = section_names['2']
    section3_title = section_names['3']

    # section2 content in between section2_title and section3_title

    # hard-coded alternatives to section2_title based on personal observations
    alternative_1 = '2. what you need to know before you are given {}'.format(product_name.lower())
    alternative_2 = '2. what you need to know before you take {}'.format(product_name.lower())
    alternative_3 = '2. what you need to know before you use {}'.format(product_name.lower())
    alternative_4 = '2 what you need to know before you take {}'.format(product_name.lower())
    alternative_5 = '2. what do you need to know before you take {}'.format(product_name.lower())
    alternative_section2_title = [alternative_1, alternative_2, alternative_3, alternative_4, alternative_5]

    try:
        # Case when section2_title from ToC matches section2_title in leaflet
        if len(leaflet.split(section2_title, 1)) == 2:
            section2_content = leaflet.split(section2_title, 1)[1]
        elif len(leaflet.split(section2_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section2_title from ToC

            flag = 0
            for alternative in alternative_section2_title:
                # check if alternative matches the section2_title in leaflet
                if len(leaflet.split(alternative, 1)) == 2:
                    flag = 1
                    section2_content = leaflet.split(alternative, 1)[1]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # hard-coded alternatives to section3_title based on personal observations
    alternative_1 = '3. how {} is given'.format(product_name.lower())
    alternative_2 = '3. how {} is given how it is given'.format(product_name.lower())
    alternative_3 = '3. how to use {}'.format(product_name.lower())
    alternative_4 = '3. how to take {}'.format(product_name.lower())
    alternative_5 = '3. how you will be given {}'.format(product_name.lower())
    alternative_6 = '3 how to take {}'.format(product_name.lower())
    alternative_7 = '3. how {} is used'.format(product_name.lower())
    alternative_section3_title = [alternative_1, alternative_2, alternative_3, alternative_4,
                                  alternative_5, alternative_6, alternative_7]

    try:
        # Case when section2_title from ToC matches section2_title in leaflet
        if len(section2_content.split(section3_title, 1)) == 2:
            section2_content = section2_content.split(section3_title, 1)[0]

        elif len(section2_content.split(section3_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section2_title from ToC

            flag = 0
            for alternative in alternative_section3_title:
                # check if alternative matches the section2_title in leaflet
                if len(section2_content.split(alternative, 1)) == 2:
                    flag = 1
                    section2_content = section2_content.split(alternative, 1)[0]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # remove whitespaces in the beginning/end of string
    section2_content = process_string(section2_content)

    return section2_content


def extract_section3(section_names, leaflet, product_name):
    """
    Extract Section3 from the leaflet_without_ToC (without table of content)

    Explanation:
    - standard (input) leaflet structure - section1_title, content_section1, section2_title, content_section2 ...
    - splitting leaflet by e.g. section1_title *has to result in* 2 parts - everything before section1_title,
    everything after section1_title; these parts correspond to 2 arrays
    - so first split leaflet by section1_title and select (2nd part) - section1_content, section2_title, section2_content
    - then split (2nd part) by section2_title and select 1st part - just section1_content
    - Repeat same approach for all other sections!

    *Assumption*: splitting by sectionN_title has always result in 2 parts - everything before sectionN_title,
    everything after sectionN_Title. If that's not the case --- smth is wrong with the structure of the leaflet,
    or there are spelling mistakes, typos in sectionN_title


    :param section_names: section titles of the package leaflet
    :param leaflet: package leaflet without the table of content
    :param product_name: name of the product
    :return: section3 content
    """

    # section titles from Table of Content
    section3_title = section_names['3']
    section4_title = section_names['4']

    # section3 content in between section3_title and section4_title

    # hard-coded alternatives to section3_title based on personal observations
    alternative_1 = '3. how {} is given'.format(product_name.lower())
    alternative_2 = '3. how {} is given how it is given'.format(product_name.lower())
    alternative_3 = '3. how to use {}'.format(product_name.lower())
    alternative_4 = '3. how to take {}'.format(product_name.lower())
    alternative_5 = '3. how you will be given {}'.format(product_name.lower())
    alternative_6 = '3 how to take {}'.format(product_name.lower())
    alternative_7 = '3. how {} is used'.format(product_name.lower())
    alternative_section3_title = [alternative_1, alternative_2, alternative_3, alternative_4,
                                  alternative_5, alternative_6, alternative_7]

    try:
        # Case when section3_title from ToC matches section3_title in leaflet
        if len(leaflet.split(section3_title, 1)) == 2:
            section3_content = leaflet.split(section3_title, 1)[1]

        elif len(leaflet.split(section3_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section3_title from ToC

            flag = 0
            for alternative in alternative_section3_title:
                # check if alternative matches the section3_title in leaflet
                if len(leaflet.split(alternative, 1)) == 2:
                    flag = 1
                    section3_content = leaflet.split(alternative, 1)[1]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # apparently section4_title "Possible side effects" is always consistent in naming (no alternatives)
    alternative_1 = '4. possible side effects'
    alternative_section4_title = [alternative_1]

    try:
        # Case when section4_title from ToC matches section4_title in leaflet
        if len(section3_content.split(section4_title, 1)) == 2:
            section3_content = section3_content.split(section4_title, 1)[0]

        elif len(section3_content.split(section4_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section4_title from ToC

            flag = 0
            for alternative in alternative_section4_title:
                # check if alternative matches the section2_title in leaflet
                if len(section3_content.split(alternative, 1)) == 2:
                    flag = 1
                    section3_content = section3_content.split(alternative, 1)[0]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # remove whitespaces in the beginning/end of string
    section3_content = process_string(section3_content)

    return section3_content


def extract_section4(section_names, leaflet, product_name):
    """
    Extract Section4 from the leaflet_without_ToC (without table of content)

    Explanation:
    - standard (input) leaflet structure - section1_title, content_section1, section2_title, content_section2 ...
    - splitting leaflet by e.g. section1_title *has to result in* 2 parts - everything before section1_title,
    everything after section1_title; these parts correspond to 2 arrays
    - so first split leaflet by section1_title and select (2nd part) - section1_content, section2_title, section2_content
    - then split (2nd part) by section2_title and select 1st part - just section1_content
    - Repeat same approach for all other sections!

    *Assumption*: splitting by sectionN_title has always result in 2 parts - everything before sectionN_title,
    everything after sectionN_Title. If that's not the case --- smth is wrong with the structure of the leaflet,
    or there are spelling mistakes, typos in sectionN_title


    :param section_names: section titles of the package leaflet
    :param leaflet: package leaflet without the table of content
    :param product_name: name of the product
    :return: section4 content
    """

    # section titles from Table of Content
    section4_title = section_names['4']
    section5_title = section_names['5']

    # section4 content in between section4_title and section5_title

    # apparently section4_title "Possible side effects" is always consistent in naming (no alternatives)
    alternative_1 = '4. possible side effects'
    alternative_section4_title = [alternative_1]

    try:
        # Case when section4_title from ToC matches section2_title in leaflet
        if len(leaflet.split(section4_title, 1)) == 2:
            section4_content = leaflet.split(section4_title, 1)[1]

        elif len(leaflet.split(section4_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section4_title from ToC

            flag = 0
            for alternative in alternative_section4_title:
                # check if alternative matches the section4_title in leaflet
                if len(leaflet.split(alternative, 1)) == 2:
                    flag = 1
                    section4_content = leaflet.split(alternative, 1)[1]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # hard-coded alternatives to section5_title based on personal observations
    alternative_1 = '5. how to store {}'.format(product_name.lower())
    alternative_2 = '5. how {} is stored'.format(product_name.lower())
    alternative_3 = '5 how to store {}'.format(product_name.lower())
    alternative_section5_title = [alternative_1, alternative_2, alternative_3]

    try:
        # Case when section5_title from ToC matches section5_title in leaflet
        if len(section4_content.split(section5_title, 1)) == 2:
            section4_content = section4_content.split(section5_title, 1)[0]

        elif len(section4_content.split(section5_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section2_title from ToC

            flag = 0
            for alternative in alternative_section5_title:
                # check if alternative matches the section2_title in leaflet
                if len(section4_content.split(alternative, 1)) == 2:
                    flag = 1
                    section4_content = section4_content.split(alternative, 1)[0]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # remove whitespaces in the beginning/end of string
    section4_content = process_string(section4_content)

    return section4_content


def extract_section5(section_names, leaflet, product_name):
    """
    Extract Section5 from the leaflet_without_ToC (without table of content)

    Explanation:
    - standard (input) leaflet structure - section1_title, content_section1, section2_title, content_section2 ...
    - splitting leaflet by e.g. section1_title *has to result in* 2 parts - everything before section1_title,
    everything after section1_title; these parts correspond to 2 arrays
    - so first split leaflet by section1_title and select (2nd part) - section1_content, section2_title, section2_content
    - then split (2nd part) by section2_title and select 1st part - just section1_content
    - Repeat same approach for all other sections!

    *Assumption*: splitting by sectionN_title has always result in 2 parts - everything before sectionN_title,
    everything after sectionN_Title. If that's not the case --- smth is wrong with the structure of the leaflet,
    or there are spelling mistakes, typos in sectionN_title


    :param section_names: section titles of the package leaflet
    :param leaflet: package leaflet without the table of content
    :param product_name: name of the product
    :return: section5 content
    """

    # section titles from Table of Content
    section5_title = section_names['5']
    section6_title = section_names['6']

    # section5 content in between section5_title and section6_title

    # hard-coded alternatives to section5_title based on personal observations
    alternative_1 = '5. how to store {}'.format(product_name.lower())
    alternative_2 = '5. how {} is stored'.format(product_name.lower())
    alternative_3 = '5 how to store {}'.format(product_name.lower())
    alternative_section5_title = [alternative_1, alternative_2, alternative_3]

    try:
        # Case when section5_title from ToC matches section5_title in leaflet
        if len(leaflet.split(section5_title, 1)) == 2:
            section5_content = leaflet.split(section5_title, 1)[1]

        elif len(leaflet.split(section5_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section5_title from ToC

            flag = 0
            for alternative in alternative_section5_title:
                # check if alternative matches the section4_title in leaflet
                if len(leaflet.split(alternative, 1)) == 2:
                    flag = 1
                    section5_content = leaflet.split(alternative, 1)[1]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # hard-coded alternatives to section6_title based on personal observations
    alternative_1 = '6. content of the pack and other information'
    alternative_2 = '6 contents of the pack and other information'
    alternative_3 = '6. contents of the pack and other information'
    alternative_section6_title = [alternative_1, alternative_2, alternative_3]

    try:
        # Case when section5_title from ToC matches section5_title in leaflet
        if len(section5_content.split(section6_title, 1)) == 2:
            section5_content = section5_content.split(section6_title, 1)[0]

        elif len(section5_content.split(section6_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section2_title from ToC

            flag = 0
            for alternative in alternative_section6_title:
                # check if alternative matches the section2_title in leaflet
                if len(section5_content.split(alternative, 1)) == 2:
                    flag = 1
                    section5_content = section5_content.split(alternative, 1)[0]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # remove whitespaces in the beginning/end of string
    section5_content = process_string(section5_content)

    return section5_content


def extract_section6(section_names, leaflet, product_name):
    """
    Extract Section6 from the leaflet_without_ToC (without table of content)

    :param section_names: section titles of the package leaflet
    :param leaflet: package leaflet without the table of content
    :param product_name: name of the product
    :return: section6 content
    """

    # section6 title from table of content
    section6_title = section_names['6']

    # hard-coded alternatives to section6_title based on personal observations
    alternative_1 = '6. content of the pack and other information'
    alternative_2 = '6 contents of the pack and other information'
    alternative_3 = '6. contents of the pack and other information'
    alternative_section6_title = [alternative_1, alternative_2, alternative_3]

    try:
        # Case when section6_title from ToC matches section6_title in leaflet
        if len(leaflet.split(section6_title, 1)) == 2:
            section6_content = leaflet.split(section6_title, 1)[1]

        elif len(leaflet.split(section6_title, 1)) == 1:
            # Case when section_title from ToC is not the same as in section_title_name in leaflet
            # Check a few alternatives to section6_title from ToC

            flag = 0
            for alternative in alternative_section6_title:
                # check if alternative matches the section2_title in leaflet
                if len(leaflet.split(alternative, 1)) == 2:
                    flag = 1
                    section6_content = leaflet.split(alternative, 1)[1]
                    break
            # if none of the alternatives matches --> give up
            if flag == 0:
                return None

        else:
            # give up
            return None
    except:
        return None

    # remove whitespaces in the beginning/end of string
    section6_content = process_string(section6_content)

    return section6_content
