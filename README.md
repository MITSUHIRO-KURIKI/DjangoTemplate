# DjangoTemplate

## What is this?
Djangoの基本的なログイン・ログアウトなどの認証、セキュリティ対策やユーザプロフィール、お問い合わせなどのアプリケーションに共通して必要となる機能を備えたテンプレートで、学習用に作成しました  
メールアドレスに関する情報の暗号化や特定IPアドレスからのアクセス遮断などセキュリティ対策も備えています

## DEMO
内容は以下のデモサイトをご覧ください(ajax、form投稿など動的な機能はローカル環境等での実行が必要です)  
[https://mitsuhiro-kuriki.github.io/DjangoTemplate/](https://mitsuhiro-kuriki.github.io/DjangoTemplate/ "デモページ")

## Other
本アプリケーションで使われる各種ライブラリのライセンスは改変したものを含めて本ライセンスには含まれません。各種ライブラリの原ライセンスに従って利用してください。

## suppl.
```
DjangoTemplate/
├─accounts
│  ├─forms
│  ├─models
│  │  └─receivers
│  └─views
│      └─send_mail
├─apps
│  ├─access_security
│  │  └─models
│  │      └─receivers
│  ├─inquiry
│  │  ├─models
│  │  │  └─receivers
│  │  └─views
│  ├─llms_chat
│  ├─summernote
│  │  └─converter
│  │      └─parts
│  └─user_properties
│      ├─models
│      └─views
├─common
│  ├─lib
│  │  ├─axes
│  │  │  ├─***
│  │  ├─social_core
│  │  │  ├─***
│  │  └─social_django
│  │      └─***
│  ├─scripts
│  └─views
├─config
│  ├─acsess_logic
│  ├─admin_protect
│  ├─extra_settings
│  └─security
├─docs
│  └─***
├─media
│  └─apps
│      ├─summernote
│      │  └─attachment
│      │      └─image
│      └─user_profile
│          └─user_icon
├─sample
│  ├─forms
│  ├─models
│  │  ├─pagenate_ajax
│  │  └─query_search
│  └─views
├─static
│  ├─apps
│  │  ├─llms
│  │  └─user_profile
│  │      └─user_icon
│  │          └─default
│  ├─dataset
│  │  └─sample
│  │      ├─Anime
│  │      └─Temperature
│  └─templates
│      ├─base
│      ├─common
│      │  ├─css
│      │  │  ├─border_bottom_effect
│      │  │  ├─bs-color
│      │  │  ├─font-utils
│      │  │  ├─form-utils
│      │  │  ├─layout-utils
│      │  │  └─scrollspy-styles
│      │  ├─func
│      │  │  ├─Back2Top
│      │  │  ├─bs-color-modes
│      │  │  ├─bs-custom-file-input
│      │  │  ├─check-confirm
│      │  │  ├─fade_in_content
│      │  │  ├─fade_in_one_word_at_a_time
│      │  │  ├─navbar
│      │  │  ├─on-click-disable
│      │  │  ├─radio-check-control
│      │  │  ├─sidenav
│      │  │  ├─text_highlight
│      │  │  └─tooltip
│      │  └─lib
│      │      ├─cytoscape-extensions
│      │      │  ├─cytoscape-navigator
│      │      │  ├─cytoscape-panzoom
│      │      │  └─layout-base
│      │      ├─select2
│      │      ├─summernote
│      │      ├─summernote-fontawesome
│      │      └─tempus-dominus
│      ├─meta_image
│      └─pages
│          ├─home
│          │  ├─css
│          │  └─img
│          └─sample
│              └─css
├─templates
│  ├─accounts
│  │  ├─AccountDelete
│  │  ├─AccountLock
│  │  ├─EmailChange
│  │  │  └─mail_template
│  │  ├─LogIn
│  │  ├─PasswordChange
│  │  ├─PasswordReset
│  │  │  └─mail_template
│  │  └─SignUp
│  │      └─mail_template
│  ├─apps
│  │  ├─inquiry
│  │  │  └─inquiry_form
│  │  │      └─notice_admin_mail_template
│  │  └─user_properties
│  │      ├─asset
│  │      │  └─sidenav
│  │      └─Settings
│  ├─common
│  │  ├─asset
│  │  │  ├─ajax_pagenation
│  │  │  ├─bs-color-modes
│  │  │  ├─cytoscape
│  │  │  ├─grecaptcha
│  │  │  ├─page_move
│  │  │  ├─summernote
│  │  │  ├─tempus-dominus
│  │  │  └─textarea_resize
│  │  └─debug
│  │      └─sample
│  │          ├─form
│  │          ├─graph
│  │          ├─items
│  │          │  └─ajax
│  │          ├─page
│  │          └─summernote_form
│  │              └─posted_items
│  └─pages
│      ├─general
│      └─home
│          └─page
│              └─not_authenticated
└─templatetags
    ├─common
    └─context_processors
```
