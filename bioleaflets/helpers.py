import numpy as np


def make_valid_mapping(package_leaflets):
    """
    Make sure to have valid mappings from NER (input) to section_content (output)

    In case either input or output - None or empty, make sure the corresponding pair is None

    :param package_leaflets: list, collection of package leaflets
    :return: package_leaflets with valid mappings
    """

    for leaflet in package_leaflets:

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        for section_index, current_section in enumerate(current_leaflet_sections):

            # if section_content is None, make sure entity_recognition is None too (can not map NER --> None)
            if current_section.section_content is None:
                current_section.entity_recognition = None
                continue

            # if entity_recognition is None, make sure section_content is None too (can not map from None --> text)
            if current_section.entity_recognition is None:
                current_section.section_content = None
                continue

            # set empty section_content to None, make sure entity_recognition is None too (can not map NER --> None)
            if len(current_section.section_content) == 0:
                current_section.section_content = None
                current_section.entity_recognition = None
                continue

            # set empty NER outputs to None, make sure section_content is None too (can not map from None --> text)
            if len(current_section.entity_recognition) == 0:
                current_section.entity_recognition = None
                current_section.section_content = None
                continue

    return package_leaflets


def remove_duplicates(package_leaflets):
    """
    Set duplicates either in section_content or entity_recognition to None

    :param package_leaflets: list, collection of package leaflets
    :return: package_leaflets without duplicates
    """

    # keep track of unique NER outputs observed so far
    unique_NER_outputs = dict()

    # keep track of unique section contents observed so far
    unique_section_content = dict()

    COUNT_DUPLICATE_NER_OUTPUTS = 0
    COUNT_DUPLICATE_SECTION_CONTENT = 0

    for leaflet in package_leaflets:

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        for section_index, current_section in enumerate(current_leaflet_sections):

            if current_section.section_content is None or current_section.entity_recognition is None:
                continue

            # set duplicate NER outputs to None

            is_duplicate_NER = False

            # get only the 'Text' of entities
            current_section_entities = ''
            for entity in current_section.entity_recognition:
                current_section_entities += entity['Text'] + ' '

            if current_section_entities not in unique_NER_outputs:
                unique_NER_outputs[current_section_entities] = 1
            else:
                unique_NER_outputs[current_section_entities] += 1
                COUNT_DUPLICATE_NER_OUTPUTS += 1
                is_duplicate_NER = True

            # set duplicate section content to None

            is_duplicate_section_content = False

            section_content = current_section.section_content

            if section_content not in unique_section_content:
                unique_section_content[section_content] = 1
            else:
                unique_section_content[section_content] += 1
                COUNT_DUPLICATE_SECTION_CONTENT += 1
                is_duplicate_section_content = True

            # set duplicate section_content or duplicate NER output to None
            if (section_index + 1) == 1:
                if is_duplicate_NER: leaflet.section1.entity_recognition = None
                if is_duplicate_section_content: leaflet.section1.section_content = None
            elif (section_index + 1) == 2:
                if is_duplicate_NER: leaflet.section2.entity_recognition = None
                if is_duplicate_section_content: leaflet.section2.section_content = None
            elif (section_index + 1) == 3:
                if is_duplicate_NER: leaflet.section3.entity_recognition = None
                if is_duplicate_section_content: leaflet.section3.section_content = None
            elif (section_index + 1) == 4:
                if is_duplicate_NER: leaflet.section4.entity_recognition = None
                if is_duplicate_section_content: leaflet.section4.section_content = None
            elif (section_index + 1) == 5:
                if is_duplicate_NER: leaflet.section5.entity_recognition = None
                if is_duplicate_section_content: leaflet.section5.section_content = None
            elif (section_index + 1) == 6:
                if is_duplicate_NER: leaflet.section6.entity_recognition = None
                if is_duplicate_section_content: leaflet.section6.section_content = None

    print('Num. of detected duplicate NER outputs:', COUNT_DUPLICATE_NER_OUTPUTS)
    print('Num. of detected duplicate section contents:', COUNT_DUPLICATE_SECTION_CONTENT)

    return package_leaflets


def calc_section_len(package_leaflets):
    """
    Calculate the average length of each section(1-6)

    :param package_leaflets: list, collection of package leaflets
    :return: dict, (key: str, section_num; value: list of lengths of corresponding sections)
    """

    # calculate length of each section

    section_content_len = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': []
    }

    # calc the length of section content and add to list
    for leaflet_idx in range(len(package_leaflets)):

        for section_idx in range(1, 7):

            if section_idx == 1:
                current_section_content = package_leaflets[leaflet_idx].section1.section_content
                if current_section_content is not None: section_content_len['1'].append(len(current_section_content))
            elif section_idx == 2:
                current_section_content = package_leaflets[leaflet_idx].section2.section_content
                if current_section_content is not None: section_content_len['2'].append(len(current_section_content))
            elif section_idx == 3:
                current_section_content = package_leaflets[leaflet_idx].section3.section_content
                if current_section_content is not None: section_content_len['3'].append(len(current_section_content))
            elif section_idx == 4:
                current_section_content = package_leaflets[leaflet_idx].section4.section_content
                if current_section_content is not None: section_content_len['4'].append(len(current_section_content))
            elif section_idx == 5:
                current_section_content = package_leaflets[leaflet_idx].section5.section_content
                if current_section_content is not None: section_content_len['5'].append(len(current_section_content))
            elif section_idx == 6:
                current_section_content = package_leaflets[leaflet_idx].section6.section_content
                if current_section_content is not None: section_content_len['6'].append(len(current_section_content))

    print('Section 1: ', np.mean(section_content_len['1']))
    print('Section 2: ', np.mean(section_content_len['2']))
    print('Section 3: ', np.mean(section_content_len['3']))
    print('Section 4: ', np.mean(section_content_len['4']))
    print('Section 5: ', np.mean(section_content_len['5']))
    print('Section 6: ', np.mean(section_content_len['6']))

    return section_content_len


def find_outliers_threshold(data, name='', m=3.5):
    """
    Standard Deviation Method

    We use 3.5 standard deviations from the mean as a cut-off for identifying outliers in data (input).

    Outliers are to the right side of the distribution

    Outliers:
    print('Outliers - Section Lengths:', data[abs(data - np.mean(data)) > m * np.std(data)])

    Check:
    print(data[abs(data - np.mean(data)) > m * np.std(data)] >= min(data[abs(data - np.mean(data)) > m * np.std(data)]))

    :param data: list
    :param name: str, description of data (e.g. section num)
    :param m: int, num. of standard deviations
    :return:
    """

    # filtered data without outliers
    filtered_data = data[abs(data - np.mean(data)) < m * np.std(data)]

    # outliers
    outliers = data[abs(data - np.mean(data)) > m * np.std(data)]

    # print - number of outliers
    print(name, len(data), '-', len(filtered_data), "=", len(outliers), '\tThreshold:', min(outliers))

    # find the threshold, section content with length > threshold ---> outliers
    return min(outliers)


def remove_outliers(package_leaflets):
    """
    Remove outliers in section content.

    Calc length of each section content.
    Find threshold for removing outliers in each section type.

    If length of section content is higher than the threshold for corresponding section type, it is an outlier.

    :param package_leaflets: list, collection of package leaflets
    :return: list, package leaflets without outliers
    """

    print("Before removing outliers:")
    section_content_len = calc_section_len(package_leaflets)

    outliers_threshold = {
        '1': find_outliers_threshold(np.array(section_content_len['1']), name='Section1:'),
        '2': find_outliers_threshold(np.array(section_content_len['2']), name='Section2:'),
        '3': find_outliers_threshold(np.array(section_content_len['3']), name='Section3:'),
        '4': find_outliers_threshold(np.array(section_content_len['4']), name='Section4:'),
        '5': find_outliers_threshold(np.array(section_content_len['5']), name='Section5:'),
        '6': find_outliers_threshold(np.array(section_content_len['6']), name='Section6:')
    }

    # set outliers in section contents to None

    for leaflet_idx in range(len(package_leaflets)):

        for section_idx in range(1, 7):

            if section_idx == 1:
                current_section_content = package_leaflets[leaflet_idx].section1.section_content
                if current_section_content is not None and len(current_section_content) >= outliers_threshold['1']:
                    package_leaflets[leaflet_idx].section1.section_content = None

            elif section_idx == 2:
                current_section_content = package_leaflets[leaflet_idx].section2.section_content
                if current_section_content is not None and len(current_section_content) >= outliers_threshold['2']:
                    package_leaflets[leaflet_idx].section2.section_content = None

            elif section_idx == 3:
                current_section_content = package_leaflets[leaflet_idx].section3.section_content
                if current_section_content is not None and len(current_section_content) >= outliers_threshold['3']:
                    package_leaflets[leaflet_idx].section3.section_content = None

            elif section_idx == 4:
                current_section_content = package_leaflets[leaflet_idx].section4.section_content
                if current_section_content is not None and len(current_section_content) >= outliers_threshold['4']:
                    package_leaflets[leaflet_idx].section4.section_content = None

            elif section_idx == 5:
                current_section_content = package_leaflets[leaflet_idx].section5.section_content
                if current_section_content is not None and len(current_section_content) >= outliers_threshold['5']:
                    package_leaflets[leaflet_idx].section5.section_content = None

            elif section_idx == 6:
                current_section_content = package_leaflets[leaflet_idx].section6.section_content
                if current_section_content is not None and len(current_section_content) >= outliers_threshold['6']:
                    package_leaflets[leaflet_idx].section6.section_content = None

    # check the mean length of each section after removing outliers
    print("After removing outliers:")
    _ = calc_section_len(package_leaflets)

    return package_leaflets


def _sort_key(entity):
    """ Key used to sort entities """
    return entity['BeginOffset']


def are_entities_ordered(package_leaflets):
    """
    Make sure detected entities for every section content are ordered

    :param package_leaflets: list, collection of package leaflets
    """

    def _test_order_entities(section_entities):
        sorted_entities = sorted(section_entities, key=_sort_key)
        if sorted_entities == section_entities: return True
        return False

    # for each leaflet
    for leaflet in package_leaflets:

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        # for each section in leaflet
        for current_section in current_leaflet_sections:

            if current_section.entity_recognition is None:
                continue

            # check that entities are sorted
            assert _test_order_entities(current_section.entity_recognition) is True, "Entities have to be sorted"


def add_entity_product_name(package_leaflets):
    """
    Make leaflet's product_name to be the first entity in entity_recognition for every section_content

    :param package_leaflets: list, collection of package leaflets
    :return: package_leaflets with update entity_recognition for each section
    """

    for leaflet in package_leaflets:

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        for section_index, current_section in enumerate(current_leaflet_sections):

            # skip None and empty detected entities
            if current_section.entity_recognition is None or len(current_section.entity_recognition) == 0:
                current_section.entity_recognition = None
                continue

            # extract results of NER
            section_entity_recognition = current_section.entity_recognition

            # add product_name as 1st Entity
            section_entity_recognition.insert(0, {'Text': leaflet.product_name.lower(), 'Type': 'PRODUCT_NAME',
                                                  'BeginOffset': 0, 'EndOffset': 0})

            # update the info in dataset
            current_section.entity_recognition = section_entity_recognition

    return package_leaflets


def count_sections(dataset):
    """
    Display number of sections depending on section type(num)

    :param dataset: list, collection of leaflets
    """

    num_sections = {
        'Section 1': 0,
        'Section 2': 0,
        'Section 3': 0,
        'Section 4': 0,
        'Section 5': 0,
        'Section 6': 0
    }

    for leaflet in dataset:

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        for section_index, current_section in enumerate(current_leaflet_sections):

            # skip None (duplicates should be skipped)
            if current_section.section_content is None or current_section.entity_recognition is None:
                continue

            if (section_index + 1) == 1: num_sections['1'] += 1
            elif (section_index + 1) == 2: num_sections['2'] += 1
            elif (section_index + 1) == 3: num_sections['3'] += 1
            elif (section_index + 1) == 4: num_sections['4'] += 1
            elif (section_index + 1) == 5: num_sections['5'] += 1
            elif (section_index + 1) == 6: num_sections['6'] += 1

    print(num_sections)
