from django.urls import path
from .chat_ajax_views import chat_ajax_view

# config.urls 逆参照
app_name = 'llms_chat'

urlpatterns = [
    path('ajax/', chat_ajax_view, name='chat'),
]