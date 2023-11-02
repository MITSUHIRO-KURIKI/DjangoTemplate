from .parts import html_revert_fnc, image_revert_fnc
from typing import List

def revert_fnc(html_text:str,
               revert_type:str               = 'id2url',
               attachment_ids_list:List[str] = []) -> str:
    """
    ## Args: 
    ### revert_type:
      * id2url(default) => 表示画面用(attachment_id -> image file)
      * id2base64       => 編集画面用(attachment_id -> byte -> base64)
    """
    is_wrap_delete = True if revert_type == 'id2base64' else False
    convered_text  = html_revert_fnc(html_text, is_wrap_delete)
    convered_text  = image_revert_fnc(convered_text, revert_type, attachment_ids_list)
    return convered_text