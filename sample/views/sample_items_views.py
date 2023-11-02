from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
import pandas as pd
from common.scripts import (
    get_pagenate_objs_and_range_list,
    preprocess_texts, create_sentence_in_words,
    calculation_jaccard, calculation_word_frequency,
    create_wordcloud,
)
from ..models import SampleAnimeDataset
from ..models.query_search import query_search

def import_anime_dataset2model(request):
    # 一旦モデルをクリア
    SampleAnimeDataset.objects.all().delete() 
    
    # csvの取り込み(一旦Nサンプリング)
    N  = 1000 # Anime.csv 21460 rows
    df = pd.read_csv('static/dataset/sample/Anime/Anime.csv', encoding='utf-8')
    for idx, row in df.head(N).iterrows():
        obj, _ = SampleAnimeDataset.objects.get_or_create(
                        Japanese = 'null' if pd.isnull(row.Japanese) else row.Japanese,
                        Synopsis = 'null' if pd.isnull(row.Synopsis) else row.Synopsis,
                        Type     = 'null' if pd.isnull(row.Type) else row.Type,
                        Episodes = 0 if pd.isnull(row.Episodes) else row.Episodes,
                        Score    = 0 if pd.isnull(row.Score) else row.Score,
                        Ranked   = 0 if pd.isnull(row.Ranked) else row.Ranked,)
        obj.save()
    del df
    return redirect('sample:items')
    
class SampleItemsListView(ListView):

    model                 = SampleAnimeDataset
    template_name         = 'common/debug/sample/items/items.html'
    pagenate_range_Nsplit = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        # GETリクエストパラメータの取得▽
        request_page     = self.request.GET.get('page',  1)
        per_page_N_items = self.request.GET.get('per_n', 10)
        request_sort     = self.request.GET.get('sort',  'asc') # or 'desc'
        request_query    = self.request.GET.get('q',     None)
        url_param = {
            'page': request_page,
            'per_n': per_page_N_items,
            'sort': request_sort,
            'q':    request_query,
        }
        # GETリクエストパラメータの取得△

        # sort ロジック▽
        sort = 'pk' if request_sort == 'asc' else '-pk'
        objs = self.model.objects.order_by(sort).all()
        # sort ロジック△
        # search ロジック▽
        if request_query:
            objs = query_search(objs, request_query)
        # search ロジック△
        
        pagenate_objs, pagenate_nav_list, pagenate_nav_page_dict = get_pagenate_objs_and_range_list(objs, request_page, per_page_N_items)
        # pagenate 情報▽
        pagenate = {
            'objs':             pagenate_objs,
            'page':             request_page,
            'nav_list':         pagenate_nav_list,
            'nav_page_dict':    pagenate_nav_page_dict,
            'nav_range':        [ x for x in range(1,
                                                   pagenate_nav_page_dict['page_count']+1 if pagenate_nav_page_dict['page_count']+1 != 0 else 1,
                                                   int(pagenate_nav_page_dict['page_count']/self.pagenate_range_Nsplit) if int(pagenate_nav_page_dict['page_count']/self.pagenate_range_Nsplit) != 0 else 1 ) ],
            'per_page_N_items': per_page_N_items,
        }
        # pagenate 情報△

        context.update({
            'AjaxEndPoint': reverse('sample:get_items_ajax'),
            'pagenate':     pagenate,
            'url_param':    url_param,
        })
        return context

class SampleItemsDetailView(DetailView):

    model               = SampleAnimeDataset
    template_name       = 'common/debug/sample/items/detail.html'
    context_object_name = 'obj'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        obj = context[self.context_object_name]
        text = obj.Synopsis
        
        text              = preprocess_texts(text)
        sentence_in_words = create_sentence_in_words(text)
        
        # 共起ネットワーク作成▽
        min_cnt      = 1
        jaccard_dict = calculation_jaccard(sentence_in_words, min_coef=0, min_cnt=min_cnt)        
        freq_dict    = calculation_word_frequency(sentence_in_words, token_length='{1,}', min_cnt=min_cnt)
        
        id_map     = {}
        nodes_data = []
        edges_data = []
        for idx, (word, freq) in enumerate(freq_dict.items()):
            id_map[word] = idx
            ID       = idx
            LABEL    = word
            fontSize = freq*15
            nodes_data.append(f' \
                id:       "n{ ID }", \
                label:    "{ LABEL }", \
                fontSize: "{ fontSize }px", \
                size:     "{ fontSize }px", \
                role:     "Node", \
            ')
            
        for idx, (pair, coef) in enumerate(jaccard_dict.items()):
            ID     = idx
            SOURCE = id_map[pair[0]]
            TARGET = id_map[pair[1]]
            lineWeight = 0.5 if coef['pair_cnt'] == 1 else coef['jaccard_coef']*10 # ペアが1つの場合には jaccard係数が 1 のため補正
            edges_data.append(f' \
                id:         "e{ ID }", \
                source:     "n{ SOURCE }", \
                target:     "n{ TARGET }", \
                lineWeight: { lineWeight }, \
                role:       "Edge", \
            ')
        # 共起ネットワーク作成△
        
        # ワードクラウド作成▽
        img_src_str = create_wordcloud(sentence_in_words)
        # ワードクラウド作成△
        
        context.update({
            'NETWORK_TYPE':           'undirected',
            'IS_USE_EXPAND_COLLAPSE': False,
            'NODES_DATA':             nodes_data,
            'EDGES_DATA':             edges_data,
            'img_src_str':            img_src_str,
            'AjaxEndPoint':           reverse('llms_chat:chat'),
        })
        return context