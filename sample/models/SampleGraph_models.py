from django.db import models

class SampleTemperatureDataset(models.Model):

    Date    = models.DateField(verbose_name  = '日付',)
    AvgTemp = models.FloatField(verbose_name = '平均気温',)
    City    = models.TextField(verbose_name  = '都市',)
    
    class Meta:
        app_label    = 'sample'
        db_table     = 'sample_temperature_dataset_model'
        verbose_name = verbose_name_plural = '03_TemperatureDataset'