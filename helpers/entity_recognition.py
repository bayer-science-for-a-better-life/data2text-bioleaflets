import pandas as pd
import numpy as np
import html
import random
from IPython.core.display import display, HTML

def html_escape(text):
    return html.escape(text)


def highlight_entities(text, entities):
    """
    text - string
    entities - dict
    """
    
    # todo - sort entities by length of text and displan text in descending order
    
    for entity in entities:
        
        entity_text = entity['Text']
        
        # number between 0.0 (fully transparent) and 1.0 (fully opaque)
        weight = 1
        
        text_highlighted = '<span style="background-color:rgba(135,206,250,' + str(weight) + ');">' \
                            + html_escape(entity_text) + '</span>'
        
        text = text.replace(entity_text, text_highlighted)
    
    # display detected entities in section content
    display(HTML(text))


def unique_entities(entities):
    """
    entities - dict
    """
    
    # init set to store unique entities
    unique_entities = set()
    
    for entity in entities:
        unique_entities.add(entity['Text'])
        
    return unique_entities

