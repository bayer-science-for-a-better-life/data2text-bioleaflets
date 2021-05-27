import pickle

import annotations.named_entity_recognition as ner

# load array of objects, where each object is a Leaflet
with open("LEAFLET_DATASET_PROCESSED.pickle", "rb") as f:
    package_leaflets = pickle.load(f)

# perform NER with different methods
package_leaflets_AWS = ner.detect_entities_medical(package_leaflets, NER_method='aws_general')
package_leaflets_ICD10CM = ner.detect_entities_medical(package_leaflets, NER_method='infer_icd10_cm')
package_leaflets_RxNorm = ner.detect_entities_medical(package_leaflets, NER_method='infer_rx_norm')

package_leaflets_Stanza = ner.detect_entities_medical(package_leaflets, NER_method='stanza')
# convert Stanza NER outputs to same format as AWS outputs
package_leaflets_Stanza = ner.reformat_stanza(package_leaflets_Stanza)

# replace None entities in NER outputs with empty string
package_leaflets_AWS = ner.replace_none_entities(package_leaflets_AWS)
package_leaflets_ICD10CM = ner.replace_none_entities(package_leaflets_ICD10CM)
package_leaflets_RxNorm = ner.replace_none_entities(package_leaflets_RxNorm)

# merge multiple NER outputs into "combined NER"

# save merged NER for each section in package_leaflets_final
with open("data_preparation/LEAFLET_DATASET_PROCESSED.pickle", "rb") as f:
    package_leaflets_final = pickle.load(f)

# for each package leaflet in array
for leaflet_idx in range(len(package_leaflets_final)):

    # for each section in a package leaflet
    for section_idx in range(1, 7):

        if section_idx == 1:
            current_section_content = package_leaflets_AWS[leaflet_idx].section1.section_content

            original_NER = package_leaflets_AWS[leaflet_idx].section1.entity_recognition.copy()
            icd10cm_NER = package_leaflets_ICD10CM[leaflet_idx].section1.entity_recognition.copy()
            rxnorm_NER = package_leaflets_RxNorm[leaflet_idx].section1.entity_recognition.copy()
            stanza_NER = package_leaflets_Stanza[leaflet_idx].section1.entity_recognition.copy()

        elif section_idx == 2:
            current_section_content = package_leaflets_AWS[leaflet_idx].section2.section_content

            original_NER = package_leaflets_AWS[leaflet_idx].section2.entity_recognition.copy()
            icd10cm_NER = package_leaflets_ICD10CM[leaflet_idx].section2.entity_recognition.copy()
            rxnorm_NER = package_leaflets_RxNorm[leaflet_idx].section2.entity_recognition.copy()
            stanza_NER = package_leaflets_Stanza[leaflet_idx].section2.entity_recognition.copy()

        elif section_idx == 3:
            current_section_content = package_leaflets_AWS[leaflet_idx].section3.section_content

            original_NER = package_leaflets_AWS[leaflet_idx].section3.entity_recognition.copy()
            icd10cm_NER = package_leaflets_ICD10CM[leaflet_idx].section3.entity_recognition.copy()
            rxnorm_NER = package_leaflets_RxNorm[leaflet_idx].section3.entity_recognition.copy()
            stanza_NER = package_leaflets_Stanza[leaflet_idx].section3.entity_recognition.copy()

        elif section_idx == 4:
            current_section_content = package_leaflets_AWS[leaflet_idx].section4.section_content

            original_NER = package_leaflets_AWS[leaflet_idx].section4.entity_recognition.copy()
            icd10cm_NER = package_leaflets_ICD10CM[leaflet_idx].section4.entity_recognition.copy()
            rxnorm_NER = package_leaflets_RxNorm[leaflet_idx].section4.entity_recognition.copy()
            stanza_NER = package_leaflets_Stanza[leaflet_idx].section4.entity_recognition.copy()

        elif section_idx == 5:
            current_section_content = package_leaflets_AWS[leaflet_idx].section5.section_content

            original_NER = package_leaflets_AWS[leaflet_idx].section5.entity_recognition.copy()
            icd10cm_NER = package_leaflets_ICD10CM[leaflet_idx].section5.entity_recognition.copy()
            rxnorm_NER = package_leaflets_RxNorm[leaflet_idx].section5.entity_recognition.copy()
            stanza_NER = package_leaflets_Stanza[leaflet_idx].section5.entity_recognition.copy()

        elif section_idx == 6:
            current_section_content = package_leaflets_AWS[leaflet_idx].section6.section_content

            original_NER = package_leaflets_AWS[leaflet_idx].section6.entity_recognition.copy()
            icd10cm_NER = package_leaflets_ICD10CM[leaflet_idx].section6.entity_recognition.copy()
            rxnorm_NER = package_leaflets_RxNorm[leaflet_idx].section6.entity_recognition.copy()
            stanza_NER = package_leaflets_Stanza[leaflet_idx].section6.entity_recognition.copy()

        # default NER output - original_NER (by aws_general method)
        # merge other entities to default one-by-one
        updated_entities = ner.merge_NERs(original_NER, icd10cm_NER)
        updated_entities = ner.merge_NERs(updated_entities, rxnorm_NER)
        updated_entities = ner.merge_NERs(updated_entities, stanza_NER)

        # detect digits as entities in current section_content
        try:
            digits_NER = ner.detect_entities_digits(current_section_content)
        except:
            digits_NER = []

        # merge digits-entities
        updated_entities = ner.merge_digits_NERs(updated_entities, digits_NER)

        # remove duplicate entities
        updated_entities_final = ner.remove_duplicate_entities(updated_entities)

        # remove overlapping entities
        updated_entities_final = ner.remove_overlapping_entities(updated_entities_final)

        # save update entities
        if section_idx == 1:
            package_leaflets_final[leaflet_idx].section1.entity_recognition = updated_entities_final
        elif section_idx == 2:
            package_leaflets_final[leaflet_idx].section2.entity_recognition = updated_entities_final
        elif section_idx == 3:
            package_leaflets_final[leaflet_idx].section3.entity_recognition = updated_entities_final
        elif section_idx == 4:
            package_leaflets_final[leaflet_idx].section4.entity_recognition = updated_entities_final
        elif section_idx == 5:
            package_leaflets_final[leaflet_idx].section5.entity_recognition = updated_entities_final
        elif section_idx == 6:
            package_leaflets_final[leaflet_idx].section6.entity_recognition = updated_entities_final

# save results
with open("datasets/LEAFLET_DATASET_PROCESSED_NER_COMBINED.pickle", "wb") as f:
    pickle.dump(package_leaflets_final, f)

