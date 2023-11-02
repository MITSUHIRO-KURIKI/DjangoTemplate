from django.shortcuts import redirect
from django.views.generic import TemplateView
from datetime import datetime as dt
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as make_subplots
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

    template_name = 'common/debug/sample/graph/graph.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objs = SampleTemperatureDataset.objects.all()
        # データの取り出し▽
        data = []
        for obj in objs:
            data.append({
                    'Date':    obj.Date,
                    'AvgTemp': obj.AvgTemp,
                    'City':    obj.City
                })
        # データの取り出し△
        
        plot_html = self.get_go_graph(data)
        
        context.update({
            'plot_fig': plot_html,
        })
        return context
    
    def get_go_graph(self, data):
        try:
            fig = go.Figure()

            # plotly.graph_objects グラフの作成▽
            data = pd.DataFrame(data).sort_values('Date', ascending=True).reset_index(drop=True)
            
            for city in list(data.City.unique()):
                _data = data[ data.City == city ]
                fig.add_trace(go.Scatter(
                    x             = _data['Date'],
                    y             = _data['AvgTemp'],
                    name          = city,
                    yaxis         = 'y1',
                    mode          = 'lines', # 'lines' or 'markers' or 'lines+markers'
                    marker        = {'size': 3,},
                    opacity       = 0.6,
                    customdata    = _data[['Date', 'AvgTemp']],
                    hovertemplate = "日付: %{customdata[0]}<br>平均気温: %{customdata[1]}",
                ))
            # plotly.graph_objects グラフの作成△
            # 見た目処理▽
            base_font_size = 15
            base_bg_color  = 'rgb(248,249,250)' # --bs-light
            graph_bg_color = 'rgb(241,243,244)'
            hover_bg_color = base_bg_color
            text_color     = '#343A40'          # --bs-gray-dark
            line_color     = text_color
            # ベース設定
            fig.update_layout(
                font          = {'size': base_font_size*.7},
                font_family   = '"Noto Sans JP", "Noto Sans", Arial, Roboto, sans-serif, "Segoe UI"',
                plot_bgcolor  = graph_bg_color,
                paper_bgcolor = base_bg_color,
                # width         = 700,
                # height        = 500,
                autosize      = True,
                margin_pad    = 0,
                margin        = {'t': 50, "b": 30, 'l': 60, 'r': 80},
                margin_autoexpand = True,
            )
            # グラフタイトル
            fig.update_layout( title = {
                'text':    '都市の平均気温の推移',
                'font':    { 'size': base_font_size*.9, 'color': text_color },
                'xref':    'container', # 'container', 'paper'
                'x':       .5,
                'y':       .95,
                'xanchor': 'center',}
            )
            # 凡例
            fig.update_layout(
                showlegend = True,
                legend     = {
                    'title':      '都市',
                    'xanchor':    'left',
                    'yanchor':    'bottom',
                    'x':           1.01,
                    'y':           .75,
                    'orientation': 'v', # h or v
                    'bgcolor':     base_bg_color,
                    'bordercolor': base_bg_color,
                    'borderwidth': 1,}
            )
            # hover
            fig.update_layout(
                hovermode = 'x', # 'x', 'y', 'closest', False, 'x unified', 'y unified'
                hoverlabel = {
                    "font":        { 'size': base_font_size*.6 },
                    'bgcolor':     hover_bg_color,
                    'bordercolor': line_color},
            )
            # marker
            fig.update_traces(marker ={
                    'size': 3,
                    'line': {
                        'width': 1,
                        'color': line_color,},
                    },
                    selector = {'mode': 'markers'},
            )
            # 軸
            fig.update_layout( xaxis = {
                'title':      '日付',
                'tickformat': '%y/%m',
                'dtick':      'M1',
                'autorange':  True}
            )
            fig.update_xaxes(
                showline  = False,
                linewidth = 1,
                linecolor = line_color,
                color     = text_color,
            )
            fig.update_layout( yaxis = {
                'title': '日付',
                'dtick':  5,}
            )
            fig.update_yaxes(
                showline  = False,
                linewidth = 1,
                linecolor = line_color,
                color     = text_color,
            )
            # 見た目処理△
            plot_html = fig.to_html(
                            include_plotlyjs = False,
                            full_html        = False,
                            div_id           = 'PlotlyGraph',
                        )
        except:
            # 主にDBが空の場合に発生する例外処理
            plot_html = '<div>No chart</div>'
        return plot_html