from django.core.files.base import ContentFile
import base64
from bs4 import BeautifulSoup
import copy
from typing import Tuple, List
from uuid import uuid4
from ...models import SummernoteAttachment

def image_converter_uplode_image(image_tag:str) -> Tuple[str, str]:
    
    attachment_id = uuid4().hex
    image_b64     = image_tag.get('src').split('base64,')[1]
    image_type    = image_tag.get('src').split('data:image/')[1].split(';')[0]
    img_name      = attachment_id+'.'+image_type
    
    # base64 -> byte -> image_object
    image_byte = base64.b64decode(image_b64)
    image_obj  = ContentFile(image_byte)
    
    self_model = SummernoteAttachment.objects.create(attachment_id=attachment_id)
    self_model.image_file.save(img_name, image_obj)
    
    image_tag.attrs['src'] = self_model.attachment_id
    
    return image_tag, attachment_id

def image_converter_replace_src(html_text:str) -> Tuple[str, List]:
    attachment_ids=[]
    soup = BeautifulSoup(html_text, "html.parser")
    
    for image_tag in soup.find_all("img"):

        if image_tag.get('attachment_id'):
            # Update時 attachment_id があればそのまま src に追加
            # MEMO: 本番運用時には 画像が URL 表記だがここでアップロードされた画像か判断する
            attachment_id = image_tag.get('attachment_id')
            _image_tag = copy.copy(image_tag)
            _image_tag.attrs['src'] = attachment_id
            del _image_tag.attrs['attachment_id']
            
            soup = str(soup).replace(str(image_tag),str(_image_tag))
            attachment_ids.append(attachment_id)
        
        elif not image_tag.get('src').startswith(('http://', 'https://')):
            # base64 の画像を モデルに追加
            _image_tag = copy.copy(image_tag)
            _image_tag, attachment_id = image_converter_uplode_image(_image_tag)
            
            soup = str(soup).replace(str(image_tag),str(_image_tag))
            attachment_ids.append(attachment_id)
        
        else:
            # attachment_id がなく、かつ URL の場合にはそのまま通過
            continue

    return str(soup), attachment_ids

def image_modify_fnc(html_text:str,
                    attachment_ids_list:List[str] = []) -> Tuple[str, List]:
    
    convered_text, attachment_ids = image_converter_replace_src(html_text)

    # 編集で削除された画像をモデルからも削除
    delete_attachment_ids = list(set(attachment_ids_list) - set(attachment_ids))
    SummernoteAttachment.objects.filter(attachment_id__in=delete_attachment_ids).all().delete()

    # 紐付ける レコードの object を返す
    create_attachment_model_object = SummernoteAttachment.objects.filter(attachment_id__in=attachment_ids).all()
    return convered_text, create_attachment_model_object