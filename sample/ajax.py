from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from common.scripts.LlmUtils import Llm
from common.scripts.NLPUtils import (
    preprocess_texts, create_sentence_in_words,
    create_wordcloud,
)
from common.scripts.PythonCodeUtils import print_color
from .models import SampleAnimeDataset

@require_http_methods(['POST'])
# @login_required
@csrf_protect
def llm_summary_ajax(request):
    
    # POSTリクエストパラメータの取得▽
    title    = request.POST.get('title',   None)
    Synopsis = request.POST.get('Synopsis', '')
    # POSTリクエストパラメータの取得△

    if settings.DEBUG:
        print_color('info: Run OpenAI Script', 3)
    try:
        llm = Llm(temperature       = 1.0,
                  model_name        = 'gpt-3.5-turbo',
                  api_key           = settings.OPENAI_API_KEY,
                  azure_endpoint    = settings.AZURE_OPENAI_ENDPOINT if settings.IS_USE_AZURE_OPENAI else None,
                  azure_api_version = settings.AZURE_OPENAI_ENDPOINT if settings.IS_USE_AZURE_OPENAI else None,)

        response = llm.get_response(
                        user_sentence = f"""
                                        The following sentences is an overview of the anime "{ title }".
                                        Please briefly summarize the sentences and please let me know if you have any additional information other than the sentences.

                                        # sentences:
                                        ```
                                        { Synopsis }
                                        ```
                                        """,
                        system_sentence = 'You are an expert who is very knowledgeable about Japanese anime. Please keep your answer short.',)
        
        status = 'success'
    except:
        response = None
        status   = 'false'

    response_data = {
        'status':   status,
        'response': response,
    }
    return JsonResponse(response_data, safe=False)


@require_http_methods(['POST'])
# @login_required
@csrf_protect
def create_wordcloud_ajax(request):
    
    # POSTリクエストパラメータの取得▽
    data_pk = request.POST.get('data_pk', None)
    # POSTリクエストパラメータの取得△

    if settings.DEBUG:
        print_color('info: Run WordCloud Script', 3)
    
    if data_pk:
        obj  = get_object_or_404(SampleAnimeDataset, pk=data_pk)

        text              = preprocess_texts(obj.Synopsis)
        sentence_in_words = create_sentence_in_words(text)
        
        img_src_str = create_wordcloud(sentence_in_words,
                                       font_path = 'common/fonts/Noto_Sans_JP/NotoSansJP-VariableFont_wght.ttf',)
        status = 'success'
    else:
        img_src_str = None
        status      = 'false'
    
    response_data = {
        'status':      status,
        'img_src_str': img_src_str,
    }
    return JsonResponse(response_data, safe=False)