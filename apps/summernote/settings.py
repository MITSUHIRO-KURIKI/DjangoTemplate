# 許可するタグのリスト
ALLOWED_TAGS = [
    'a', 'div', 'p', 'span', 'img', 'em', 'i', 'li', 'ol', 'ul', 'strong', 'br', 'hr', 'font',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'table', 'tbody', 'thead', 'tr', 'td',
    'abbr', 'acronym', 'b', 'blockquote', 'pre', 'code', 'strike', 'u', 'sup', 'sub',
    'iframe',
]
# 許可する属性
ATTRIBUTES = {
    '*':      ['class', 'style', 'color', 'align', 'title',],
    'div':    ['id', 'class', ],
    'a':      ['href', 'target', 'rel',],
    'img':    ['src', 'attachment_id',],
    'iframe': ['src', 'width', 'height',],
}
# 許可するCSSスタイルのリスト
ALLOWED_STYLES = [
    'background-color', 'font-size', 'line-height', 'color', 'text-align', 'font-family', 'width', 'height', 'margin-left',
]
#  許可するリンクのプロトコル
ALLOWED_PROTOCOLS = frozenset(('http', 'https', 'data'))
# 許可していない要素を除去する
IS_STRIP = True
# HTMLコメントを除去する
IS_STRIP_COMMENT = True
# iframe で許可するsrcドメイン
YOUTUBE_DOMAIN        = ['www.youtube.com', 'youtube.com',]
INSTAGRAM_DOMAIN      = ['www.instagram.com', 'instagram.com',]
ALLOWED_IFRAME_DOMAIN = YOUTUBE_DOMAIN + INSTAGRAM_DOMAIN
# アップロードする画像のリサイズ設定
RESIZE_WIDTH  = 300
# html内容を囲うclass(css等での装飾のみに使用)
WRAP_ClassName = 'SummernoteTextArea'