from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),  # Route for the welcome page
    path('soil-analysis/', views.soil_analysis_view, name='soil_analysis'),  # URL for the soil analysis view
]


