# analysis/logic/main.py
import os
import django
import serial
import time
import json  # Added for Arduino JSON parsing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soil_django.settings')
django.setup()
from analysis.logic.crop_rec import get_crop_recommendation, get_crop_accuracy
from analysis.logic.fertilizer import recommend_fertilizer, get_fertilizer_accuracy
from analysis.logic.soil_analysis import (
    predict_soil_type, predict_npk, calculate_soil_score, 
    soil_suitability_message, get_soil_type_accuracy, predict_salinity
)
from analysis.models import SoilAnalysis, CropRecommendation, FertilizerRecommendation

# Function to store predictions into SQLite database
def store_predictions(predicted_soil_type, npk, soil_score, suitability_message, salinity, recommended_crop, recommended_fertilizer):
    # Save Soil Analysis Data
    soil_analysis_entry = SoilAnalysis.objects.create(
        soil_type=predicted_soil_type,
        nitrogen=npk['Nitrogen'],
        phosphorus=npk['Phosphorus'],
        potassium=npk['Potassium'],
        soil_score=soil_score
    )

    # Save Crop Recommendation Data
    crop_entry = CropRecommendation.objects.create(
        soil_type=predicted_soil_type,
        recommended_crop=recommended_crop
    )

    # Save Fertilizer Recommendation Data
    fertilizer_entry = FertilizerRecommendation.objects.create(
        soil_type=predicted_soil_type,
        recommended_fertilizer=recommended_fertilizer
    )

    print("Predicted data successfully stored in the database!")

# ------------------- UPDATED get_user_input() -------------------
# Arduino Serial Setup
SERIAL_PORT = "COM3"  # Change if needed
BAUD_RATE = 9600

# Open serial port once (avoid opening multiple times)
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to initialize
    print(f"Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    ser = None
    print(f"Failed to connect to Arduino: {e}")

def get_user_input():
    """Return live sensor data from Arduino if available, else default values"""
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                sensor_data = json.loads(line)
                # Map Arduino keys to your expected keys
                return {
                    'Electrical Conductivity (dS/m)': 0.7,  # Keep default EC
                    'Moisture (%)': sensor_data.get('Moisture', 6.8),
                    'pH': 5.1,  # Keep default pH
                    'Temperature (°C)': sensor_data.get('Temperature', 18.37),
                    'Humidity (%)': sensor_data.get('Humidity', 49)
                }
        except Exception as e:
            print(f"Error reading Arduino data: {e}")

    # Fallback to defaults if no Arduino data
    return {
        'Electrical Conductivity (dS/m)': 0.7,
        'Moisture (%)': 6.8,
        'pH': 5.1,
        'Temperature (°C)': 18.37,
        'Humidity (%)': 49
    }
# -----------------------------------------------------------------

# Main function to run the entire analysis
def run_soil_analysis():
    # Step 1: Predict Soil Type
    predicted_soil_type = predict_soil_type(get_user_input())

    # Step 2: Predict NPK Values
    npk = predict_npk(get_user_input(), predicted_soil_type)

    # Step 3: Calculate Soil Score and Suitability
    soil_score = calculate_soil_score(npk)
    suitability_message = soil_suitability_message(soil_score)

    # Step 4: Predict Salinity
    salinity = predict_salinity(get_user_input(), predicted_soil_type)

    # Step 5: Get Crop Recommendation
    recommended_crop = get_crop_recommendation(get_user_input(), predicted_soil_type, npk, salinity)

    # Step 6: Recommend Fertilizer
    recommended_fertilizer = recommend_fertilizer(get_user_input(), predicted_soil_type, npk, salinity, recommended_crop)

    # Step 7: Save Results to Database
    store_predictions(predicted_soil_type, npk, soil_score, suitability_message, salinity, recommended_crop, recommended_fertilizer)

    fertilizer_accuracy = get_fertilizer_accuracy()

    # Step 8: Display Results
    print("\n--- Soil Analysis Results ---")
    print(f"Predicted Soil Type: {predicted_soil_type}")
    print(f"Predicted Nitrogen: {npk['Nitrogen']:.2f} mg/kg")
    print(f"Predicted Phosphorus: {npk['Phosphorus']:.2f} mg/kg")
    print(f"Predicted Potassium: {npk['Potassium']:.2f} mg/kg")
    print(f"Predicted Salinity: {salinity:.2f} ppm")
    print(f"Soil Score: {soil_score:.2f}")
    print(f"Soil Suitability Message: {suitability_message}")
    print(f"Recommended Crop: {recommended_crop}")
    print(f"Recommended Fertilizer: {recommended_fertilizer}")
    print(f"Fertilizer Model Accuracy: {fertilizer_accuracy:.2%}")

# Run the analysis
if __name__ == "__main__":
    run_soil_analysis()
