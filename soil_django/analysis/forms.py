from django import forms

class SoilAnalysisForm(forms.Form):
    soil_moisture = forms.FloatField(label='Soil Moisture (%)')
    temperature = forms.FloatField(label='Temperature (°C)')
    ph = forms.FloatField(label='pH Level')
    organic_carbon = forms.FloatField(label='Organic Carbon (%)')
    electrical_conductivity = forms.FloatField(label='Electrical Conductivity (dS/m)')
    humidity = forms.FloatField(label='Humidity (%)')
