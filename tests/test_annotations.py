import pickle
import statistics

from EMA_documents import SectionLeaflet, Leaflet
from test_bioleaflets_preparation import *


def count_none_values(package_leaflets_ner):

    COUNT_NONE_section_content = 0
    COUNT_NONE_section_entities = 0

    for leaflet in package_leaflets_ner:

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        for current_section in current_leaflet_sections:

            if current_section.section_content is None:
                COUNT_NONE_section_content += 1

            if current_section.entity_recognition is None:
                COUNT_NONE_section_entities += 1

    print("Section Content is None: ", COUNT_NONE_section_content)
    print("Entity Recognition is None: ", COUNT_NONE_section_entities)

    return COUNT_NONE_section_entities


def calc_duplicate_NER(package_leaflets_ner):
    """
    find out the number of duplicate NER outputs
    """

    # Keep Track of NER outputs
    # (key, value) -
    # (NER_output, (num.occurences, section_indices containing NER_output , product_names(leaflets) containing NER_output))
    NER_outputs = dict()

    COUNT_DUPLICATE_NER_OUTPUTS = 0

    # for each leaflet
    for leaflet in package_leaflets_ner:

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        # for each section in a leaflet
        for section_index, current_section in enumerate(current_leaflet_sections):

            # skip None and empty sections
            if current_section.section_content is None or len(current_section.section_content) <= 1:
                continue

            # get only the 'Text' of entities
            current_section_entities = ''
            for entity in current_section.entity_recognition:
                current_section_entities += entity['Text'] + ' '

            # save to a dict unique NER outputs
            if current_section_entities not in NER_outputs:
                NER_outputs[current_section_entities] = (1, [section_index + 1], [leaflet.product_name])

            # if current_section_entities is in NER_outputs - then it is a duplicate
            else:
                prev_num = NER_outputs[current_section_entities][0]

                # add the section index of the duplicate NER output to a list
                prev_indices = NER_outputs[current_section_entities][1]
                prev_indices.append(section_index + 1)

                # add the product_name of the duplicate NER output to a list
                prev_names = NER_outputs[current_section_entities][2]
                prev_names.append(leaflet.product_name)

                NER_outputs[current_section_entities] = (prev_num + 1, prev_indices, prev_names)
                COUNT_DUPLICATE_NER_OUTPUTS += 1

    COUNT_NONE_section_entities = count_none_values(package_leaflets_ner)

    print("The total number of duplicate NER Outputs: ", COUNT_DUPLICATE_NER_OUTPUTS)
    print("Total num. of NER outputs: ", len(package_leaflets_ner) * 6 - COUNT_NONE_section_entities)
    print("The total number of duplicate section contents discovered during NER:   153 (including empty sections)")

    return NER_outputs


def display_duplicate_NER(package_leaflets_ner):

    NER_outputs = calc_duplicate_NER(package_leaflets_ner)

    # sort the NER outputs by the number of occurrences (descending order)
    NER_outputs_sorted = dict(sorted(NER_outputs.items(), key=lambda item: item[1], reverse=True))

    # save duplicate NER_OUTPUTS that appear more than once in NER_outputs
    DUPLICATE_NER_OUTPUTS = []

    # total number of occurences of duplicate NER outputs
    TOTAL_NUMBER_DUPLICATE_NER_OUTPUTS = 0

    # for each NER output in dictionary
    for entities in NER_outputs_sorted:

        # in case NER output appears more than 1 - it is a duplicate
        if NER_outputs_sorted[entities][0] != 1:

            # display entities that appear more than N number of times
            # print(entities, " -------------------> ", NER_outputs_sorted[entities][0], ", section index-",
            #      statistics.mode(NER_outputs_sorted[entities][1]), ", products-", NER_outputs_sorted[entities][2])
            # print()

            # count current NER output as the one having duplicates
            DUPLICATE_NER_OUTPUTS.append(entities)

            # count how many times each duplicate NER output appears
            # -1 since the 1st occurence of a NER output is considered to be unique
            TOTAL_NUMBER_DUPLICATE_NER_OUTPUTS += NER_outputs_sorted[entities][0] - 1

    print("Number of NER outputs that appear more than once: ", len(DUPLICATE_NER_OUTPUTS))


def display_duplicate_section(package_leaflets_ner):

    NER_outputs = calc_duplicate_NER(package_leaflets_ner)

    # sort the NER outputs by the number of occurrences (descending order)
    NER_outputs_sorted = dict(sorted(NER_outputs.items(), key=lambda item: item[1], reverse=True))

    DUPLICATE_NER_OUTPUT_SECTION1 = 0
    DUPLICATE_NER_OUTPUT_SECTION2 = 0
    DUPLICATE_NER_OUTPUT_SECTION3 = 0
    DUPLICATE_NER_OUTPUT_SECTION4 = 0
    DUPLICATE_NER_OUTPUT_SECTION5 = 0
    DUPLICATE_NER_OUTPUT_SECTION6 = 0

    # for each NER output in dictionary
    for entities in NER_outputs_sorted:

        # in case NER output appears more than 1 - it is a duplicate
        if NER_outputs_sorted[entities][0] != 1:

            num_occurrences = NER_outputs_sorted[entities][0]
            duplicate_NER_output_indices = NER_outputs_sorted[entities][1]

            assert len(duplicate_NER_output_indices) == num_occurrences

            # first index is considered to be unique NER output
            for index in duplicate_NER_output_indices[1:]:
                if index == 1:
                    DUPLICATE_NER_OUTPUT_SECTION1 += 1
                elif index == 2:
                    DUPLICATE_NER_OUTPUT_SECTION2 += 1
                elif index == 3:
                    DUPLICATE_NER_OUTPUT_SECTION3 += 1
                elif index == 4:
                    DUPLICATE_NER_OUTPUT_SECTION4 += 1
                elif index == 5:
                    DUPLICATE_NER_OUTPUT_SECTION5 += 1
                elif index == 6:
                    DUPLICATE_NER_OUTPUT_SECTION6 += 1

    print("Occurrences of duplicate NER output in Section1", DUPLICATE_NER_OUTPUT_SECTION1)
    print("Occurrences of duplicate NER output in Section2", DUPLICATE_NER_OUTPUT_SECTION2)
    print("Occurrences of duplicate NER output in Section3", DUPLICATE_NER_OUTPUT_SECTION3)
    print("Occurrences of duplicate NER output in Section4", DUPLICATE_NER_OUTPUT_SECTION4)
    print("Occurrences of duplicate NER output in Section5", DUPLICATE_NER_OUTPUT_SECTION5)
    print("Occurrences of duplicate NER output in Section6", DUPLICATE_NER_OUTPUT_SECTION6)


# load array of leaflets with detected entities
with open("LEAFLET_DATASET_NER_AWS.pickle", "rb") as f:
    package_leaflets_ner = pickle.load(f)
