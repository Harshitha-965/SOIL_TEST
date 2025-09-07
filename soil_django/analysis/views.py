from django.shortcuts import render
from analysis.logic.soil_analysis import predict_soil_type, predict_npk, calculate_soil_score, soil_suitability_message, predict_salinity
from analysis.logic.crop_rec import get_crop_recommendation
from analysis.logic.fertilizer import recommend_fertilizer
from analysis.logic.main import get_user_input  # Import input function


def soil_analysis_view(request):
    # Get user input from main.py
    user_input = get_user_input()

    # Step 1: Predict Soil Type
    predicted_soil_type = predict_soil_type(user_input)

    # Step 2: Predict NPK Values
    npk = predict_npk(user_input, predicted_soil_type)

    # Step 3: Calculate Soil Score and Suitability
    soil_score = calculate_soil_score(npk)
    soil_suitability = soil_suitability_message(soil_score)

    # Step 4: Predict Salinity
    salinity = predict_salinity(user_input, predicted_soil_type)

    # Step 5: Get Crop Recommendation
    recommended_crop = get_crop_recommendation(user_input, predicted_soil_type, npk, salinity)

    # Step 6: Recommend Fertilizer
    recommended_fertilizer = recommend_fertilizer(user_input, predicted_soil_type, npk, salinity, recommended_crop)

    # Prepare context data to send to template
    
    context = {
        'soil_type': predicted_soil_type,
        'npk': npk,
        'soil_score': soil_score,
        'soil_suitability': soil_suitability,
        'recommended_crop': recommended_crop,
        'recommended_fertilizer': recommended_fertilizer,
    }

    # Render the template with context data
    return render(request, 'analysis/soil_analysis_output.html', context)

def welcome(request):
    return render(request, 'analysis/welcome.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import serial
import time

# Define the Serial Port and Baud Rate
SERIAL_PORT = "COM3"  # Change for Linux: "/dev/ttyACM0"
BAUD_RATE = 9600

def get_arduino_data():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for the connection to stabilize

        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received Data: {data}")  # Debugging
            sensor_data = json.loads(data)  # Convert JSON string to dictionary
            return sensor_data
    except Exception as e:
        print(f"Error: {e}")

    return None

@csrf_exempt
def fetch_sensor_data(request):
    """API Endpoint to get real-time sensor data from Arduino"""
    sensor_data = get_arduino_data()
    if sensor_data:
        return JsonResponse(sensor_data, safe=False)
    else:
        return JsonResponse({"error": "No data received"}, status=500)
