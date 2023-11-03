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
│  │  ├─social_core
│  │  └─social_django
│  ├─scripts
│  └─views
├─config
│  ├─acsess_logic
│  ├─admin_protect
│  ├─extra_settings
│  └─security
├─docs
├─media
│  └─apps
├─sample
│  ├─forms
│  ├─models
│  │  ├─pagenate_ajax
│  │  └─query_search
│  └─views
├─static
│  ├─apps
│  ├─dataset
│  └─templates
│      ├─base
│      ├─common
│      │  ├─css
│      │  ├─func
│      │  └─lib
│      ├─meta_image
│      └─pages
│          ├─home
│          └─sample
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
│  │      └─Settings
│  ├─common
│  │  ├─asset
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
└─templatetags
```
