"""

TO-DO:

- test add_entity_product_name(package_leaflets)

for leaflet_idx in range(len(package_leaflets)):

    for section_idx in range(1,7):

        if section_idx == 1: current_entities = package_leaflets[leaflet_idx].section1.entity_recognition
        elif section_idx == 2: current_entities = package_leaflets[leaflet_idx].section2.entity_recognition
        elif section_idx == 3: current_entities = package_leaflets[leaflet_idx].section3.entity_recognition
        elif section_idx == 4: current_entities = package_leaflets[leaflet_idx].section4.entity_recognition
        elif section_idx == 5: current_entities = package_leaflets[leaflet_idx].section5.entity_recognition
        elif section_idx == 6: current_entities = package_leaflets[leaflet_idx].section6.entity_recognition

        if current_entities is not None:
            assert current_entities[0]['Type'] == 'PRODUCT_NAME'



"""