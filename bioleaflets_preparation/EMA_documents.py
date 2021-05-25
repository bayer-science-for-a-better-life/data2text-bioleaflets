"""
Represent classes found in European Medicines Agency (EMA) documents
"""


class SectionLeaflet:
    """
    Class to represent individual section of a Package Leaflet
    """

    def __init__(self, title, section_content, entity_recognition=None):
        self.title = title
        self.section_content = section_content
        self.is_duplicate = False
        self.entity_recognition = entity_recognition
        self.generated_content = None

    def print_original_info(self):
        """ Display original information about a section """

        print("The name of the section: \n", self.title, "\n===================\n")
        print("Original content of the section: \n", self.section_content, "\n===================\n")

    def print_entities(self):
        """ Print entities of the current section with corresponding Category, Type and Confidence Score """

        if self.entity_recognition is not None:
            for entity in self.entity_recognition:
                print("{0} ({1}, type: {2}, score:{3:.2f})".format(entity["Text"],
                                                                   entity["Category"],
                                                                   entity["Type"],
                                                                   entity["Score"]))

    def compare_contents(self):
        """ Compare original content of a section to generated content """

        print("Original Content: \n", self.section_content, "\n===================\n")
        print("Generated Content: \n", self.generated_content, "\n===================\n")

    def print_all_info(self):
        """ Display all information about a section """

        print("The name of the section: \n", self.title, "\n===================\n")
        print("Original content of the section: \n", self.section_content, "\n===================\n")
        print("Named entity recognition: \n", self.entity_recognition, "\n===================\n")
        print("Generated content of the section: \n", self.generated_content, "\n===================\n")


class Leaflet:
    """
    Class to represent Package Leaflet, containing 6 sections
    """

    def __init__(self, product_name, product_url, product_id, product_content,
                 section1=None, section2=None, section3=None, section4=None, section5=None, section6=None):
        # leaflet attributes
        self.product_name = product_name
        self.url = product_url
        self.id = product_id
        self.content = product_content

        # extracted sections
        self.section1 = section1
        self.section2 = section2
        self.section3 = section3
        self.section4 = section4
        self.section5 = section5
        self.section6 = section6

    def display_info(self, full_content=True):
        """ Show information about a package leaflet"""

        print("Product Name: \n", self.product_name, "\n===================\n")
        print("Url: \n", self.url, "\n===================\n")
        print("Product ID: \n", self.id, "\n===================\n")
        if full_content == True:
            print("Full Leaflet Content: \n", self.content, "\n===================\n")

    def print_section(self, section_type=None):
        """ Display a particular section of a package leaflet """

        if section_type == "1" and self.section1 is not None:
            self.section1.print_all_info()
        else:
            print("No section1 in the current leaflet - ", self.product_name)

        if section_type == "2" and self.section2 is not None:
            self.section2.print_all_info()
        else:
            print("No section2 in the current leaflet - ", self.product_name)

        if section_type == "3" and self.section3 is not None:
            self.section3.print_all_info()
        else:
            print("No section3 in the current leaflet - ", self.product_name)

        if section_type == "4" and self.section4 is not None:
            self.section4.print_all_info()
        else:
            print("No section4 in the current leaflet - ", self.product_name)

        if section_type == "5" and self.section5 is not None:
            self.section5.print_all_info()
        else:
            print("No section5 in the current leaflet - ", self.product_name)

        if section_type == "6" and self.section6 is not None:
            self.section6.print_all_info()
        else:
            print("No section6 in the current leaflet - ", self.product_name)
