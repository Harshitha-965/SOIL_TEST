from django import forms

class SoilAnalysisForm(forms.Form):
    electrical_conductivity = forms.FloatField(label="Electrical Conductivity (dS/m)")
    moisture = forms.FloatField(label="Moisture (%)")
    pH = forms.FloatField(label="pH")
    temperature = forms.FloatField(label="Temperature (°C)")
    salinity = forms.FloatField(label="Salinity (ppm)")
    humidity = forms.FloatField(label="Humidity (%)")
    nitrogen = forms.FloatField(label="Nitrogen (mg/kg)")
    phosphorus = forms.FloatField(label="Phosphorus (mg/kg)")
    potassium = forms.FloatField(label="Potassium (mg/kg)")