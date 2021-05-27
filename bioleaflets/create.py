import pickle

# split into train-dev-test
from sklearn.model_selection import train_test_split

from bioleaflets.helpers import \
    remove_duplicates, make_valid_mapping, \
    remove_outliers, are_entities_ordered, \
    add_entity_product_name, count_sections

# load array of annotated package leaflets
with open("datasets/LEAFLET_DATASET_PROCESSED_NER_COMBINED.pickle", "rb") as f:
    package_leaflets = pickle.load(f)

# make sure every sample is a valid mapping from NER_entities(non-empty) to section_content(non-empty)
package_leaflets = make_valid_mapping(package_leaflets)

# set duplicates in NER_outputs or section contents to None
package_leaflets = remove_duplicates(package_leaflets)

# remove outliers in section contents
package_leaflets = remove_outliers(package_leaflets)

# check that detected entities for each section content are ordered
are_entities_ordered(package_leaflets)

# add product_name as the 1st entity to every section
package_leaflets = add_entity_product_name(package_leaflets)

# split dataset into train-valid-test (0.9-0.1-0.1) and shuffle

# train - test
train_leaflets, test_leaflets = train_test_split(package_leaflets, test_size=0.1, random_state=42, shuffle=True)
# train - valid
train_leaflets, valid_leaflets = train_test_split(train_leaflets, test_size=134, random_state=42, shuffle=True)

# show distributions of sections in train-dev-test sets
count_sections(train_leaflets)
count_sections(valid_leaflets)
count_sections(test_leaflets)

# save results
with open("LEAFLET_TRAIN_DATASET.pickle", "wb") as f:
    pickle.dump(train_leaflets, f)

with open("LEAFLET_VALID_DATASET.pickle", "wb") as f:
    pickle.dump(valid_leaflets, f)

with open("LEAFLET_TEST_DATASET.pickle", "wb") as f:
    pickle.dump(test_leaflets, f)
