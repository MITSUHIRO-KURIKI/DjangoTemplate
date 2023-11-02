from django.conf import settings
from django.urls import reverse
from django.http.response import JsonResponse
from common.scripts import print_color
import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage, HumanMessage, SystemMessage,
)

def chat_ajax_view(request):
    
    if request.user.is_anonymous:
        chat_results = '<small>この機能を使用するにはログインしている必要があります</small>'
    else:
        # GETリクエストパラメータの取得▽
        user_sentence   = request.GET.get('user_sentence',   None)
        system_sentence = request.GET.get('system_sentence', '')
        max_tokens      = request.GET.get('max_tokens',      None)
        temperature     = request.GET.get('temperature',     0.7)
        ## MEMO: https://platform.openai.com/docs/api-reference/chat/create#chat-create-temperature
        # GETリクエストパラメータの取得△

        if settings.DEBUG:
            print_color('info: Run OpenAI Script', 3)
        try:
            chat = ChatOpenAI(model_name     = 'gpt-3.5-turbo',
                            streaming      = False,
                            max_tokens     = max_tokens,
                            temperature    = temperature,
                            openai_api_key = settings.OPENAI_API_KEY,)
            messages = [
                SystemMessage(content = system_sentence),
                HumanMessage(content  = user_sentence),
            ]
            response = chat(messages)
            chat_results = response.content # -> format: AIMessage(content='***')
        except:
            chat_results = 'error...'

    response_data = {
        'chat_results': chat_results,
    }
    return JsonResponse(response_data, safe=False)