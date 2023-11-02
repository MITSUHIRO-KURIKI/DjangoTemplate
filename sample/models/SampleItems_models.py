from django.db import models

class SampleAnimeDataset(models.Model):

    Japanese = models.TextField(verbose_name    = 'タイトル',)
    Synopsis = models.TextField(verbose_name    = '概要',)
    Type     = models.TextField(verbose_name    = 'タイプ',)
    Episodes = models.IntegerField(verbose_name = 'エピソード数',)
    Score    = models.FloatField(verbose_name   = 'スコア',)
    Ranked   = models.IntegerField(verbose_name = 'ランキング',)
    
    class Meta:
        app_label    = 'sample'
        db_table     = 'sample_anime_dataset_model'
        verbose_name = verbose_name_plural = '02_AnimeDataset'