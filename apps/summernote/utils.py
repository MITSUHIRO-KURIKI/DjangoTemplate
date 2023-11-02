from urllib.parse import urlparse

def get_domain_from_url(url:str) -> str:
    parsed_url = urlparse(url)
    domain     = parsed_url.netloc
    return domain