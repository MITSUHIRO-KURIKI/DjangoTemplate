from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from common.scripts.DjangoUtils import get_pagenate_objs_and_range_list
import json
from ...models import SampleAnimeDataset
from ..query_search import query_search

@require_http_methods(['POST'])
# @login_required
@csrf_protect
def sample_items_models_pagenate_ajax(request):
    print(request)
    
    # POSTリクエストパラメータの取得▽
    request_page     = int(request.POST.get('request_page', 1))
    per_page_N_items = int(request.POST.get('per_n',        10))
    request_query    = request.POST.get('q',                None)
    request_sort     = 'asc' if request.POST.get('sort',    'asc') == 'asc' else 'desc'
    # POSTリクエストパラメータの取得△

    # sort ロジック▽
    sort = 'pk' if request_sort == 'asc' else '-pk'
    objs = SampleAnimeDataset.objects.order_by(sort).all()
    # sort ロジック△
    # search ロジック▽
    if request_query:
        objs = query_search(objs, request_query)
    # search ロジック△
    
    pagenate_objs, pagenate_nav_list, pagenate_nav_page_dict = get_pagenate_objs_and_range_list(objs, request_page, per_page_N_items)

    objs_data_list = []
    for obj in pagenate_objs:
        data_json             = {'url':'/', 'Japanese':'load error',}
        data_json['pk']       = obj.pk
        data_json['url']      = reverse('sample:item_detail', kwargs={'pk': obj.pk} )
        data_json['Japanese'] = obj.Japanese
        objs_data_list.append(data_json)
    
    response_data = {
        'status':        'success',
        'objs_data':     json.dumps(objs_data_list),
        'nav_list':      pagenate_nav_list,
        'nav_page_dict': pagenate_nav_page_dict,
    }
    return JsonResponse(response_data, safe=False)