# analysis/admin.py

from django.contrib import admin
from .models import SoilAnalysis, CropRecommendation, FertilizerRecommendation

# Register your models here
admin.site.register(SoilAnalysis)
admin.site.register(CropRecommendation)
admin.site.register(FertilizerRecommendation)