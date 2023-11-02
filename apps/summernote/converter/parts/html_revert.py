from bs4 import BeautifulSoup
from ...settings import WRAP_ClassName

def delete_wrap_ClassName_tag(html_text:str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    wrap_content = []
    for wrap in soup.find_all("div", class_ = WRAP_ClassName):
        wrap_content += wrap.contents
    return ''.join(map(str, wrap_content))

def html_revert_fnc(html_text:str,
                    is_wrap_delete:bool = False,) -> str:
    if is_wrap_delete:
        html_text = delete_wrap_ClassName_tag(html_text)
    else:
        pass
    return html_text