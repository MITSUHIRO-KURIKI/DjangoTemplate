from django.contrib import admin
from .models import (
    SampleSummernotePost, SampleAnimeDataset, SampleTemperatureDataset,
)

admin.site.register(SampleSummernotePost)
admin.site.register(SampleAnimeDataset)
admin.site.register(SampleTemperatureDataset)