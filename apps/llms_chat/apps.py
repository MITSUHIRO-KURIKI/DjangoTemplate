from django.apps import AppConfig


class LlmsChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    name         = 'apps.llms_chat'
    verbose_name = '80_LlmsChat'