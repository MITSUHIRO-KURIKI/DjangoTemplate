from django.urls import path
from common.views import ScrollSpyTemplateView
from .views import (
    SampleFormView,
    SampleSummernotePostCreateView, SampleSummernotePostDetailView,
    SampleSummernotePostUpdateView, SampleSummernotePostDeleteView,
    import_anime_dataset2model,
    SampleItemsListView, SampleItemsDetailView,
    import_temperature_dataset2model, SampleGraphView,
)
from .models.pagenate_ajax import get_sample_items_ajax_data

# config.urls 逆参照
app_name = 'sample'

urlpatterns = [
    # scloll spy 動作確認用ページ
    path('page/', ScrollSpyTemplateView(template_name='common/debug/sample/page/page.html',), name='page'),
    # 動作確認用フォーム
    path('form/', SampleFormView.as_view(), name='form'),
    # sumernote 動作確認用フォーム
    path('summernote/create/',
         SampleSummernotePostCreateView.as_view(), name='summernote_create'),
    path('summernote/detail/<int:pk>/',
         SampleSummernotePostDetailView.as_view(), name='summernote_detail'),
    path('summernote/update/<int:pk>/',
         SampleSummernotePostUpdateView.as_view(), name='summernote_update'),
    path('summernote/delete/<int:pk>/',
         SampleSummernotePostDeleteView,           name='summernote_delete'),
    # pagenation querysearch 動作確認用ページ
    path('items/import_dataset/',  import_anime_dataset2model,      name='import_anime_dataset'),
    path('items/ajax/pagenate',    get_sample_items_ajax_data,      name='get_items_ajax'),
    path('items/',                 SampleItemsListView.as_view(),   name='items'),
    path('items/detail/<int:pk>/', SampleItemsDetailView.as_view(), name='item_detail'),
    # plotly 動作確認用ページ
    path('graph/import_dataset/',  import_temperature_dataset2model, name='import_temperature_dataset'),
    path('graph/',                 SampleGraphView.as_view(),        name='graph'),
]