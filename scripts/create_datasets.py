import pickle
from nltk.tokenize import wordpunct_tokenize


def create_source_target(dataset, section_condition=None):
    """
    Create train-dev-test files for T5 fine-tuning.

    From HuggingFace:
    If you are using your own data for fine-tuning, it must be formatted as one directory with 6 files:
    test.source, test.target
    train.source, train.target
    val.source, val.target

    The .source files are the input (entities), the .target files are the desired output (section contents).

    :param dataset: list, collection of package leaflets
    :param section_condition: None, 'section', 'semantic', specify the type of additional condition used in input.
    :return: source_data_array, target_data_array: array of source samples and corresponding target samples
    """

    if section_condition is not None and section_condition not in ['section', 'semantic']:
        print('section_condition must be either None or \'section\' or \'semantic\'')
        return

    # array to store source data of each leaflet
    source_data_array = []

    # array to store target data of each leaflet
    target_data_array = []

    for leaflet in dataset:

        current_leaflet_sections = [leaflet.section1, leaflet.section2,
                                    leaflet.section3, leaflet.section4,
                                    leaflet.section5, leaflet.section6]

        for section_index, current_section in enumerate(current_leaflet_sections):

            # skip sample if either input or output is None
            if current_section.section_content is None or current_section.entity_recognition is None:
                continue

            # extract section content
            section_content = current_section.section_content

            # extract results of NER
            section_entity_recognition = current_section.entity_recognition

            # if condition - 'semantic' - on a section_type (section title)
            # depending on the Section index, add corresponding tag - section_title
            if section_condition == 'semantic':

                if (section_index + 1) == 1: source_leaflet_str = 'What the medicine is and what it is used for: '.lower()
                elif (section_index + 1) == 2: source_leaflet_str = 'What you need to know before you take the medicine: '.lower()
                elif (section_index + 1) == 3: source_leaflet_str = 'How to take the medicine: '.lower()
                elif (section_index + 1) == 4: source_leaflet_str = 'Possible side effects: '.lower()
                elif (section_index + 1) == 5: source_leaflet_str = 'How to store the medicine: '.lower()
                elif (section_index + 1) == 6: source_leaflet_str = 'Contents of the pack and other information: '.lower()

            # if condition - 'section' - on a section index (section num.)
            elif section_condition == 'section':

                if (section_index + 1) == 1: source_leaflet_str = 'section 1: '.lower()
                elif (section_index + 1) == 2: source_leaflet_str = 'section 2: '.lower()
                elif (section_index + 1) == 3: source_leaflet_str = 'section 3: '.lower()
                elif (section_index + 1) == 4: source_leaflet_str = 'section 4: '.lower()
                elif (section_index + 1) == 5: source_leaflet_str = 'section 5: '.lower()
                elif (section_index + 1) == 6: source_leaflet_str = 'section 6: '.lower()

            # no condition
            else:
                # start with empty string
                source_leaflet_str = ''

            for entity in section_entity_recognition:

                entity_value = entity['Text'] if len(entity['Text'].split(" ")) == 0 \
                    else ("_").join(entity['Text'].split(" "))
                entity_type = entity['Type'] if entity['Type'] is not None and len(entity['Type']) > 0 \
                    else entity['Category']

                # create source data in special format (with tags)
                source_leaflet_str += "<" + str(entity_type) + "> " + str(entity_value) + " </" + str(entity_type) + ">"

                if section_entity_recognition.index(entity) != len(section_entity_recognition) - 1:
                    # 1 whitespace - delimiter between entities
                    source_leaflet_str += " "
                else:
                    # after last entity insert "\n"
                    source_leaflet_str += "\n"

            # add current source sample to array
            source_data_array.append(source_leaflet_str)

            # make sure to have punctuations as a separate token
            section_content = wordpunct_tokenize(section_content)

            # back to string
            section_content = " ".join(section_content)

            # add "\n" at the end of target text
            section_content = section_content + "\n"

            # add current target sample to array
            target_data_array.append(section_content)

    return source_data_array, target_data_array


def save_data_file(data, filename):
    """
    Save data to the file
    """

    FILE_PATH = filename

    # save to corresponding file
    output_file = open(FILE_PATH, 'w')
    for leaflet_data in data:
        output_file.write(leaflet_data)
    output_file.close()

    print("Data saved successfully to ", filename)
    print("=====================================")


# load array of leaflets - training dataset
with open("datasets/LEAFLET_TRAIN_DATASET.pickle", "rb") as f:
    train_dataset = pickle.load(f)

# load array of leaflets - validation dataset
with open("datasets/LEAFLET_VALID_DATASET.pickle", "rb") as f:
    valid_dataset = pickle.load(f)

# load array of leaflets - test dataset
with open("datasets/LEAFLET_TEST_DATASET.pickle", "rb") as f:
    test_dataset = pickle.load(f)

# create source, target files for train-dev-test
source_train, target_train = create_source_target(train_dataset, section_condition=None)
source_valid, target_valid = create_source_target(valid_dataset, section_condition=None)
source_test, target_test = create_source_target(test_dataset, section_condition=None)


# Train
TRAIN_SOURCE='~/data2text-bioleaflets/scripts/data/train.source'
save_data_file(source_train, TRAIN_SOURCE)

TRAIN_TARGET='~/data2text-bioleaflets/scripts/data//train.target'
save_data_file(target_train, TRAIN_TARGET)

# Validation
VAL_SOURCE='~/data2text-bioleaflets/scripts/data/val.source'
save_data_file(source_valid, VAL_SOURCE)

VAL_TARGET='~/data2text-bioleaflets/scripts/data/val.target'
save_data_file(target_valid, VAL_TARGET)

# Test
TEST_SOURCE='~/data2text-bioleaflets/scripts/data/test.source'
save_data_file(source_test, TEST_SOURCE)

TEST_TARGET='~/data2text-bioleaflets/scripts/data/test.target'
save_data_file(target_test, TEST_TARGET)
