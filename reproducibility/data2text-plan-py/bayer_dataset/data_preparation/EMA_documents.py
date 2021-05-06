"""
Represent classes found in European Medicines Agency (EMA) documents
"""


class SectionLeaflet:
    def __init__(self, title, section_content, entity_recognition):
        self.title = title
        self.section_content = section_content
        self.entity_recognition = entity_recognition

    def get_info(self):
        print("The name of the section: \n", self.title, "\n===================\n")
        print("The content of the section: \n", self.section_content, "\n===================\n")
        print("Named entity recognition: \n", self.entity_recognition, "\n===================\n")


class Leaflet:
    def __init__(self, product_name, product_url, product_id, product_content, section1_obj=None):
        self.product_name = product_name
        self.url = product_url
        self.id = product_id
        self.content = product_content

        # extract sections later
        self.section1 = section1_obj

    def display_info(self):
        print("Product Name: \n", self.product_name, "\n===================\n")
        print("Url: \n", self.url, "\n===================\n")
        print("Product ID: \n", self.id, "\n===================\n")
        print("Content: \n", self.content, "\n===================\n")

    def print_section1(self):
        if self.section1 is not None:
            self.section1.get_info()
        else:
            print("No section1 in the current leaflet")

