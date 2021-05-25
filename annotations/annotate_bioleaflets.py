# perform NER with AWS Comprehend
import boto3

# perform NER with Stanford Stanza
import stanza

import pickle
import numpy as np
import re
from EMA_documents import SectionLeaflet, Leaflet


def detect_entities(package_leaflets, NER_method, output_path=None):
    """
    Perform Named Entity Recognition with AWS Comprehend or Stanford Stanza for each section in every leaflet

    :param package_leaflets: list, array of leaflets
    :param NER_method: AWS service used for NER (e.g. aws_general, infer_icd10_cm, infer_rx_norm, stanza)
    :param output_path: str, path to a pickle file where to save results
    :return: list, array of leaflets with detected entities for each section
    """

    if NER_method in ['aws_general', 'infer_icd10_cm', 'infer_rx_norm']:
        # init AWS client
        client = boto3.client(service_name='comprehendmedical', region_name='us-east-1')

    elif NER_method == 'stanza':
        # download mimic package with an i2b2 NER model
        stanza.download('en', package='mimic', processors={'ner': 'i2b2'})

        # initialize a mimic pipeline with an i2b2 NER model
        nlp_pipeline = stanza.Pipeline('en', package='mimic', processors={'ner': 'i2b2'})

    else:
        print("NER_method must be either 'aws_general' or'infer_icd10_cm' or 'infer_rx_norm' or 'stanza")
        return

    # save (unique_section, NER output) as (key, value) pairs
    unique_sections = dict()

    for leaflet_index, leaflet in enumerate(package_leaflets):

        # Progress Bar
        print("Processing: ", leaflet.product_name, leaflet.id)
        if leaflet_index % 100 == 0:
            print(" =============== Number of Document Processed: {}".format(leaflet_index + 1))

        current_leaflet_sections = [leaflet.section1.section_content, leaflet.section2.section_content,
                                    leaflet.section3.section_content, leaflet.section4.section_content,
                                    leaflet.section5.section_content, leaflet.section6.section_content]

        for section_index, current_section in enumerate(current_leaflet_sections):

            # skip None Sections
            if current_section is None:
                continue

            # check whether current section is a duplicate section
            if current_section in unique_sections:
                # get NER output from the dict
                entities_current_section = unique_sections[current_section]
                print("DUPLICATE SECTION ", section_index + 1, ": ", leaflet.product_name, leaflet.id)

            # if not duplicate section - Perform NER
            else:
                entities_current_section = None

                if current_section is not None and len(current_section) > 1:
                    # get the detected entities for current section

                    if NER_method == "aws_general":
                        AWS_response = client.detect_entities_v2(Text=current_section)
                        entities_current_section = AWS_response['Entities']

                    elif NER_method == "infer_icd10_cm":
                        try:
                            AWS_response = client.infer_icd10_cm(Text=current_section)
                            entities_current_section = AWS_response['Entities']
                        except Exception as error:
                            print('Failed infer_icd10_cm NER for Section', section_index + 1, ' ----> ', error)
                            entities_current_section = None

                    elif NER_method == "infer_rx_norm":
                        try:
                            AWS_response = client.infer_rx_norm(Text=current_section)
                            entities_current_section = AWS_response['Entities']
                        except Exception as error:
                            print('Failed infer_rx_norm NER for Section', section_index + 1, ' ----> ', error)
                            entities_current_section = None

                    elif NER_method == "stanza":
                        try:
                            ner_annotations = nlp_pipeline(current_section).entities
                            entities_current_section = ner_annotations
                        except Exception as error:
                            print('Failed Stanza NER for Section', section_index + 1, ' ----> ', error)
                            entities_current_section = None

                # store (section, entities_section) in a dict
                unique_sections[current_section] = entities_current_section

            # save the detected entities in SectionLeaflet
            if (section_index + 1) == 1:
                leaflet.section1.entity_recognition = entities_current_section
            elif (section_index + 1) == 2:
                leaflet.section2.entity_recognition = entities_current_section
            elif (section_index + 1) == 3:
                leaflet.section3.entity_recognition = entities_current_section
            elif (section_index + 1) == 4:
                leaflet.section4.entity_recognition = entities_current_section
            elif (section_index + 1) == 5:
                leaflet.section5.entity_recognition = entities_current_section
            elif (section_index + 1) == 6:
                leaflet.section6.entity_recognition = entities_current_section

    # save results to a file
    if output_path:
        with open(output_path, "wb") as f:
            pickle.dump(package_leaflets, f)

    return package_leaflets


def format_stanza(package_leaflets_Stanza):
    """ Stanza entity not a dict but - <class 'stanza.models.common.doc.Span'> """

    for leaflet_index, leaflet in enumerate(package_leaflets_Stanza):

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        for section_index, current_section in enumerate(current_leaflet_sections):

            if current_section.section_content is None:
                current_section.entity_recognition = []
                continue

            ### set empty section content to None
            if len(current_section.section_content) <= 1:
                current_section.section_content = None
                current_section.entity_recognition = []
                continue

            if current_section.entity_recognition is None:
                current_section.entity_recognition = []
                continue

            if len(current_section.entity_recognition) < 1:
                current_section.entity_recognition = []
                continue

            formatted_stanza_NER = []

            for entity in current_section.entity_recognition:
                formatted_entity = {'Text': entity.text, 'Type': entity.type, 'BeginOffset': entity.start_char,
                                    'EndOffset': entity.end_char}
                formatted_stanza_NER.append(formatted_entity)

            # update
            current_section.entity_recognition = formatted_stanza_NER


def replace_none_entities(leaflets_NER):
    """ replace None values with empty string """

    for leaflet_index, leaflet in enumerate(leaflets_NER):

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        for section_index, current_section in enumerate(current_leaflet_sections):

            if current_section.section_content is None:
                current_section.entity_recognition = []
                continue

            # set empty section content to None
            if len(current_section.section_content) < 1:
                current_section.section_content = None
                current_section.entity_recognition = []
                continue

            if current_section.entity_recognition is None:
                current_section.entity_recognition = []
                continue

            if len(current_section.entity_recognition) < 1:
                current_section.entity_recognition = []
                continue


def detect_entities_digits(section_content):
    """ Treat digits as entities """

    # return empty if section_content is None
    if section_content is None:
        return []

    # find all digits in seciton_content
    digits = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", section_content)

    # save digit as tuple (digit, BeginOffset, EndOffset)
    digits_entities = set()

    # simple tokenization (by " ") - better than - wordpunct_tokenize(section_content)
    tokenized_section = section_content.split()

    for token in tokenized_section:

        # if token is indeed a digit
        if token in digits:

            # find all occurrences of a token in section_content
            all_token_occurrences = [m.start() for m in re.finditer(token, section_content)]

            for occurrence in all_token_occurrences:
                # occurrence - index where current token(digit) starts in text
                left_char = occurrence - 1
                right_char = occurrence + len(token)

                # token(digit) has to be surrounded by whitespaces (ideally) or any punctuations from left and right
                try:
                    if not section_content[left_char].isalpha() and not section_content[right_char].isalpha() and not \
                    section_content[left_char].isdigit() and not section_content[right_char].isdigit():
                        # that's a digit - save it
                        digits_entities.add((token, occurrence, right_char))
                except:
                    pass

        # case when there is a punctuation symbol after the digit '122,' (address the limitation of simple tokenization)
        elif token[:-1] in digits:
            # remove the last punctuation symbol from token(digit) and do same steps as above
            token = token[:-1]

            all_token_occurrences = [m.start() for m in re.finditer(token, section_content)]

            for occurrence in all_token_occurrences:
                # occurrence - index where current digit starts in text
                left_char = occurrence - 1
                right_char = occurrence + len(token)

                # basically accept whitespaces + punctuiations
                try:
                    if not section_content[left_char].isalpha() and not section_content[right_char].isalpha() and not \
                    section_content[left_char].isdigit() and not section_content[right_char].isdigit():
                        # that's a digit - save it
                        digits_entities.add((token, occurrence, right_char))
                except:
                    pass

    return digits_entities


def _sort_key(entity):
    """ Key used in sorting enitites """
    return entity['BeginOffset']


def merge_NERs(NER_original, NER_additional):
    """

    Merge multiple NER outputs into "combined NER"

    Strategy
    - Add new entities one-by-one to existing entities (while adding make sure it is indeed a new entity)
    - Sort all entities by 'BeginOffset'
    - Save merged NER in package_leaflets_final

    :param NER_original: primary detected entities
    :param NER_additional: potential entities that could be added to  NER_original
    :return: merged entities from NER_additional into NER_original
    """

    # default NER
    NER_final = NER_original.copy()

    # lookup table
    entity_positions = dict()
    for entity in NER_final:
        entity_positions[(entity['BeginOffset'], entity['EndOffset'])] = entity

    # now add additional NERs
    for new_entity in NER_additional:

        new_entity_text = new_entity['Text']
        new_entity_start = new_entity['BeginOffset']
        new_entity_end = new_entity['EndOffset']

        # find identical - skip
        if (new_entity_start, new_entity_end) in entity_positions:
            continue

        # make sure candidate_entity (new_entity) does not overlap with other entities (alrady existing ones)
        is_overlapping = False

        # check for overlapping with existing entities
        for existing_entity in NER_original:
            existing_entity_start = existing_entity['BeginOffset']
            existing_entity_end = existing_entity['EndOffset']

            # candidate entity (new entity) is overlapping with existing entities by either 'BeginOffset' or 'EndOffset'
            # do not add candidate entity (new entity) - keep the existing one
            if new_entity_start in range(existing_entity_start, existing_entity_end + 1) or new_entity_end in range(
                    existing_entity_start, existing_entity_end + 1):
                is_overlapping = True

            # favor longer entities
            if new_entity_start == existing_entity_start and new_entity_end > existing_entity_end:
                NER_final.remove(existing_entity)
                NER_final.append(new_entity)
                is_overlapping = True
                continue

            if new_entity_end == existing_entity_end and new_entity_start < existing_entity_start:
                NER_final.remove(existing_entity)
                NER_final.append(new_entity)
                is_overlapping = True
                continue

            # case when a candidate entity (new_entity) is "wider" than already existing one
            # keep longer NER than shorter (basically - favor Stanza NER over AWS)
            if existing_entity_start in range(new_entity_start, new_entity_end + 1) and existing_entity_end in range(
                    new_entity_start, new_entity_end + 1):
                NER_final.remove(existing_entity)
                NER_final.append(new_entity)
                is_overlapping = True
                continue

            # note: do not care if candidate entity is inside the existing one

        # new entity has no overlap with existing entities, just add new separate entity
        if not is_overlapping: NER_final.append(new_entity)

    # sort entities by 'BeginOffset'
    NER_final = sorted(NER_final, key=_sort_key)

    return NER_final


def merge_digits_NERs(updated_entities, digits_NER):
    """ Add entities as digits to existing NER output """

    for digit_entity in digits_NER:
        digit_text = str(digit_entity[0])
        digit_start = digit_entity[1]
        digit_end = digit_entity[2]

        entity_digit = {'Text': digit_text, 'Type': 'NUMBER', 'BeginOffset': digit_start, 'EndOffset': digit_end}

        updated_entities.append(entity_digit)

    # sort entities by 'BeginOffset'
    updated_entities = sorted(updated_entities, key=_sort_key)

    return updated_entities


def remove_duplicate_entities(updated_entities):
    # lookup table for unique entities
    entity_positions = dict()

    # remove duplicates
    for entity_ind in range(len(updated_entities)):
        entity_text = updated_entities[entity_ind]['Text']
        entity_start = updated_entities[entity_ind]['BeginOffset']
        entity_end = updated_entities[entity_ind]['EndOffset']

        if (entity_start, entity_end) in entity_positions:
            # that's a duplicate - set entity to None
            updated_entities[entity_ind] = None
        else:
            entity_positions[(entity_start, entity_end)] = updated_entities[entity_ind]

    # now get rid off 'None'
    updated_entities_final = [entity for entity in updated_entities if entity is not None]

    # sort entities by 'BeginOffset'
    updated_entities_final = sorted(updated_entities_final, key=_sort_key)

    return updated_entities_final


def remove_overlapping_entities(updated_entities):
    # favor "longer" entities when dealing with overlapping

    assert sorted(updated_entities, key=_sort_key) == updated_entities

    for curr_ind in range(len(updated_entities)):

        if updated_entities[curr_ind] is None: continue

        curr_entity_start = updated_entities[curr_ind]['BeginOffset']
        curr_entity_end = updated_entities[curr_ind]['EndOffset']

        for next_ind in range(curr_ind + 1, len(updated_entities)):

            if updated_entities[next_ind] is None: continue

            next_entity_start = updated_entities[next_ind]['BeginOffset']
            next_entity_end = updated_entities[next_ind]['EndOffset']

            # find overlapping entities
            # entities must be separate
            if curr_entity_start in range(next_entity_start, next_entity_end + 1) or curr_entity_end in range(
                    next_entity_start, next_entity_end + 1):
                # keep the longer entity in case of overlapping
                range_curr = curr_entity_end - curr_entity_start
                range_next = next_entity_end - next_entity_start

                if range_next > range_curr:
                    # remove curr
                    updated_entities[curr_ind] = None
                else:
                    # remove next
                    updated_entities[next_ind] = None

    # now get rid off 'None'
    updated_entities_final = [entity for entity in updated_entities if entity is not None]

    # sort entities by 'BeginOffset'
    updated_entities_final = sorted(updated_entities_final, key=_sort_key)

    return updated_entities_final



# load array of objects, where each object is a Leaflet
with open("LEAFLET_DATASET_PROCESSED.pickle", "rb") as f:
    package_leaflets = pickle.load(f)


# perform NER with different methods
package_leaflets_NER = detect_entities(package_leaflets, NER_method='aws_general')
package_leaflets_ICD10CM = detect_entities(package_leaflets, NER_method='infer_icd10_cm')
package_leaflets_RxNorm = detect_entities(package_leaflets, NER_method='infer_rx_norm')

package_leaflets_Stanza = detect_entities(package_leaflets, NER_method='stanza')
# convert Stanza NER outputs to a suitable format
format_stanza(package_leaflets_Stanza)

# preprocessing NER outputs
replace_none_entities(package_leaflets_NER)
replace_none_entities(package_leaflets_ICD10CM)
replace_none_entities(package_leaflets_RxNorm)

# merge multiple NER outputs into "combined NER"

# save merged NER for each section in package_leaflets_final
with open("data_preparation/LEAFLET_DATASET_PROCESSED.pickle", "rb") as f:
    package_leaflets_final = pickle.load(f)

# To-do - one file - main code, here define only functions

