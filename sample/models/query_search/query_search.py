from django.db.models import Q
from common.scripts.DjangoUtils import parse_search_params
from functools import reduce

def query_search(objs, query:str):
    search_words_list = parse_search_params(query)
    query             = reduce(
                            lambda x,y : x & y,
                            list(map(lambda z: Q(Japanese__icontains=z), search_words_list))
                        )
    return objs.filter(query)