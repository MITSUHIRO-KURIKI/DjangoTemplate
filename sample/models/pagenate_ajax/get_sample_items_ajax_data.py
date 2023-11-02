from django.urls import reverse
from django.http.response import JsonResponse
from common.scripts import get_pagenate_objs_and_range_list
import json
from ...models import SampleAnimeDataset
from ..query_search import query_search


def get_sample_items_ajax_data(request):
    
    # GETリクエストパラメータの取得▽
    request_page     = int(request.GET.get('request_page', 1))
    per_page_N_items = int(request.GET.get('per_n',        10))
    request_sort     = request.GET.get('sort',             'asc') # or 'desc'
    request_query    = request.GET.get('q',                None)
    # GETリクエストパラメータの取得△

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
        'objs_data':     json.dumps(objs_data_list),
        'nav_list':      pagenate_nav_list,
        'nav_page_dict': pagenate_nav_page_dict,
    }
    return JsonResponse(response_data, safe=False)