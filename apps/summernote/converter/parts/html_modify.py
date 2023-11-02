from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
import bleach
from bleach.css_sanitizer import CSSSanitizer
from bs4 import BeautifulSoup
import copy
import re
from ...settings import (
    ALLOWED_TAGS, ATTRIBUTES, ALLOWED_STYLES,
    ALLOWED_PROTOCOLS, IS_STRIP, IS_STRIP_COMMENT,
    ALLOWED_IFRAME_DOMAIN, YOUTUBE_DOMAIN, WRAP_ClassName,
)
from ...utils import get_domain_from_url

User = get_user_model()


# aタグの target rel の変更
def anker_rendered_harmless(html_text:str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    for anker_tag in soup.find_all('a'):
        _anker_tag                 = copy.copy(anker_tag)
        _anker_tag.attrs['target'] = '_blank'
        _anker_tag.attrs['rel']    = 'noopener noreferrer'
        soup = str(soup).replace(str(anker_tag), str(_anker_tag))
    return str(soup)

# summernote の以下の issue に対応するもの
# https://github.com/summernote/summernote/issues/3252
def youtube_url_modification(src:str) -> str:
    if src.startswith('//'):
        src = 'https:' + src
    elif src.startswith('http://'):
        src = 'https:' + src[-7]
    else:
        pass
    return src

# iframe タグ(動画埋込)のうち許可されていないドメインのものを削除
def iframe_rendered_harmless(html_text:str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    for iframe_tag in soup.find_all('iframe'):
        domain = get_domain_from_url(iframe_tag.get('src'))
        if domain in ALLOWED_IFRAME_DOMAIN:
            if domain in YOUTUBE_DOMAIN:
                _iframe_tag              = copy.copy(iframe_tag)
                _iframe_tag.attrs['src'] = youtube_url_modification(_iframe_tag.get('src'))
                soup = str(soup).replace(str(iframe_tag), str(_iframe_tag))
            else:
                continue
        else:
            soup = str(soup).replace(str(iframe_tag), '')
    return str(soup)

# 許可されていないタグの除去
def html_rendered_harmless(html_text:str) -> str:
    return bleach.clean(html_text,
                        tags           = ALLOWED_TAGS,
                        attributes     = ATTRIBUTES,
                        css_sanitizer  = CSSSanitizer(allowed_css_properties=ALLOWED_STYLES),
                        protocols      = ALLOWED_PROTOCOLS,
                        strip          = IS_STRIP,
                        strip_comments = IS_STRIP_COMMENT,)

# wrap id(css等での装飾用)
def add_wrap_ClassName_tag(html_text:str) -> str:
    wrap_start = f'<div class="{WRAP_ClassName}">'
    wrap_end   = '</div>'
    if not html_text.startswith(wrap_start):
        return wrap_start + html_text + wrap_end
    else:
        return html_text

def html_modify_fnc(html_text:str) -> str:
    html_text = anker_rendered_harmless(html_text)
    html_text = iframe_rendered_harmless(html_text)
    html_text = html_rendered_harmless(html_text)
    html_text = add_wrap_ClassName_tag(html_text)
    return html_text

# コメント中のメンションをユーザページなどへのリンクへ変更
# 以下は sample 状況に応じて変更
# def comment2mention(text):

#     # This should allow for better coding with hard coding!
#     account_page_url = settings.FRONTEND_URL+reverse('***')

#     # comment2mention
#     p = r'(\@\S*\ )'
#     r = re.findall(p,text)
#     if len(r) > 0:
#         for mention in r:
#             unique_account_id = mention[1:-1]
#             try:
#                 user              = get_object_or_404(User, unique_account_id=unique_account_id)
#                 unique_account_id = user.unique_account_id
#                 text              = text.replace(mention, f'<a href="{account_page_url}{unique_account_id}">@{unique_account_id}</a> ')
#             except:
#                 pass
#     convert_text = text
#     return convert_text