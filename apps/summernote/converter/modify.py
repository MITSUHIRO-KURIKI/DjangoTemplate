from .parts import html_modify_fnc, image_modify_fnc
from typing import Tuple, List

def modify_fnc(html_text:str,
               attachment_ids_list:List[str] = []) -> Tuple[str, List]:
    convered_text                                 = html_modify_fnc(html_text)
    convered_text, create_attachment_model_object = image_modify_fnc(convered_text, attachment_ids_list)
    return convered_text, create_attachment_model_object