from django.shortcuts import redirect
from django.views.generic import TemplateView
from datetime import datetime as dt
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as make_subplots
from common.scripts.PlotlyUtils import get_go_line_graph
from ..models import SampleTemperatureDataset


def import_temperature_dataset2model(request):
    # 一旦モデルをクリア
    SampleTemperatureDataset.objects.all().delete() 
    
    # csvの取り込み(一旦Nサンプリング)
    city_list = ['Tokyo', 'Osaka', 'Yokohama']
    for city in city_list:
        df = pd.read_csv(f'static/dataset/sample/Temperature/{city}.csv', encoding='utf-8')
        # 日付フォーマット処理とフィルタリング▽
        start_date = '2020/1/1'
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
        df         = df[ df.Date > dt.strptime(start_date, '%Y/%m/%d') ].reset_index(drop=True)
        # 日付フォーマット処理とフィルタリング△
        for idx, row in df.iterrows():
            obj, _ = SampleTemperatureDataset.objects.get_or_create(
                            Date     = '1900-01-01' if pd.isnull(row.Date) else row.Date,
                            AvgTemp  =  0 if pd.isnull(row.AvgTemp) else row.AvgTemp,
                            City     = city,)
            obj.save()
        del df
    return redirect('sample:graph')

class SampleGraphView(TemplateView):

    template_name = 'sample/graph/graph.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objs = SampleTemperatureDataset.objects.all()
        # データの取り出し▽
        data_list = []
        data_df   = None
        for obj in objs:
            data_list.append({
                    'Date':    obj.Date,
                    'AvgTemp': obj.AvgTemp,
                    'City':    obj.City
                })
        if data_list != []:
            data_df = pd.DataFrame(data_list).sort_values('Date', ascending=True).reset_index(drop=True)\
                                             .pivot(index='Date', columns='City', values='AvgTemp').reset_index(drop=False)
        # データの取り出し△
        
        plot_html = get_go_line_graph(data_df,
                                      y_col_name  = 'Date',
                                      title       = '都市の平均気温の推移',
                                      mode        ='lines',
                                      margin      = {'t': 50, "b": 30, 'l': 60, 'r': 80},
                                      xaxis_title = '日付',
                                      xaxis_tickformat = '%y/%m',
                                      xaxis_dtick = 'M1',
                                      yaxis_dtick = 5,
                                      )
        
        context.update({
            'plot_fig': plot_html,
        })
        return context