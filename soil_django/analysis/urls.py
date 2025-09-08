from django.urls import path
from .views import soil_analysis_view, welcome, contact

urlpatterns = [
    path('', welcome, name='welcome'),
    path('soil-analysis/', soil_analysis_view, name='soil_analysis_view'),
    path('contact/', contact, name='contact'),
]

