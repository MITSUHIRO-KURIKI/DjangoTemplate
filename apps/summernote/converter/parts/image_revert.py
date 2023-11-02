from ...models import SummernoteAttachment
import base64
from bs4 import BeautifulSoup
import copy
from common.scripts import print_color
from typing import Dict

# Summernote 表示画面用
# attachment_id -> image file
def html_image_id2url_decoder(encoded_html_text:str,
                              attachment_ids_urls_dict:Dict[str,str]={},) -> str:
    soup = BeautifulSoup(encoded_html_text, "html.parser")
    for image_tag in soup.find_all("img"):
        _image_tag = copy.copy(image_tag)
        attachment_id = _image_tag.get('src')
        # image が URL の場合にはそのまま通過
        if not attachment_id.startswith(('http://', 'https://')):
            if not attachment_ids_urls_dict == {}:
                # 通常使用の想定ケース: こっちのほうが処理が早いはず
                _image_tag.attrs['src'] = attachment_ids_urls_dict[attachment_id]
            else:
                # attachment_ids_urls_dict が渡されなかった場合の処理
                print_color('warning(summernote.image_decoder.html_image_id2url_decoder): Processing with attachment_ids_urls_dict is preferable', 3)
                _image_tag.attrs['src'] = SummernoteAttachment.objects.filter(attachment_id=attachment_id).first().image_file.url
            soup = str(soup).replace(str(image_tag),str(_image_tag))
        else:
            continue
    return str(soup)

# Summernote 編集画面用
# attachment_id -> byte -> base64
def html_image_id2base64_decoder(encoded_html_text:str) -> str:
    soup = BeautifulSoup(encoded_html_text, "html.parser")
    for image_tag in soup.find_all("img"):
        _image_tag = copy.copy(image_tag)
        attachment_id = _image_tag.get('src')
        # image が URL の場合にはそのまま通過
        if not attachment_id.startswith(('http://', 'https://')):
            # image_object -> byte -> base64
            image_file = SummernoteAttachment.objects.filter(attachment_id=attachment_id).first().image_file
            image_type = image_file.url.split('.')[-1].lower()
            image_byte = base64.b64encode(image_file.read())
            image_b64  = image_byte.decode('utf-8')
            src        = f'data:image/{image_type};base64,{image_b64}'
            
            _image_tag.attrs['src'] = src
            _image_tag.attrs['attachment_id'] = attachment_id
            
            soup = str(soup).replace(str(image_tag),str(_image_tag))
        else:
            continue
    return str(soup)

def image_revert_fnc(encoded_html_text:str,
                     revert_type:str                        = 'id2url',
                     attachment_ids_urls_dict:Dict[str,str] = {},) -> str:
    """
    ## Args: 
    ### revert_type:
      * id2url(default) => 表示画面用(attachment_id -> image file)
      * id2base64       => 編集画面用(attachment_id -> byte -> base64)
    """
    if revert_type == 'id2url':
        encoded_html_text = html_image_id2url_decoder(encoded_html_text, attachment_ids_urls_dict)
    elif revert_type == 'id2base64':
        encoded_html_text = html_image_id2base64_decoder(encoded_html_text)
    else:
        raise ValueError('revert_type must be "id2url" or "id2base64"')
    return encoded_html_text