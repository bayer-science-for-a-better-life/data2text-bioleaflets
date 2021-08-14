"""
Functionality to process the extracted (raw) data from documents
"""

import pickle
import re

from EMA_documents import SectionLeaflet, Leaflet
import clean_text


# load array of objects, where object - class Leaflet
with open("LEAFLET_DATASET.pickle", "rb") as f:
    package_leaflets_raw = pickle.load(f)

print("Number of documents obtained after running create_dataset.py: ", len(package_leaflets_raw))
print("Number of documents with all sections - None:  ", clean_text.check_none_documents(package_leaflets_raw))

# in section6 remove part after 'marketing authorisation holder'
package_leaflets = clean_text.process_section6(package_leaflets_raw)

# preprocess each section in a leaflet
for leaflet in package_leaflets:

    # process Section1
    section1_processed = clean_text.process_content(leaflet.section1.section_content)
    leaflet.section1.section_content = section1_processed

    # process Section2
    section2_processed = clean_text.process_content(leaflet.section2.section_content)
    leaflet.section2.section_content = section2_processed

    # process Section3
    section3_processed = clean_text.process_content(leaflet.section3.section_content)
    leaflet.section3.section_content = section3_processed

    # process Section4
    section4_processed = clean_text.process_content(leaflet.section4.section_content)
    leaflet.section4.section_content = section4_processed

    # process Section5
    section5_processed = clean_text.process_content(leaflet.section5.section_content)
    leaflet.section5.section_content = section5_processed

    # process Section6
    section6_processed = clean_text.process_content(leaflet.section6.section_content)
    leaflet.section6.section_content = section6_processed

# remove duplicate leaflets from dataset
package_leaflets_unique = clean_text.remove_duplicates(package_leaflets)

# find out number of empty sections
clean_text.empty_sections(package_leaflets_unique)

# check the minimum number of duplicate sections
# set the section.is_duplicate = True if section is duplicate
package_leaflets_unique = clean_text.check_duplicate_sections(package_leaflets_unique,
                                                              mark_duplicate_section=True)

# save processed Leaflets to a file
with open("LEAFLET_DATASET_PROCESSED.pickle", "wb") as f:
    pickle.dump(package_leaflets_unique, f)
