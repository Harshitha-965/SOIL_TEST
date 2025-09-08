from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from analysis.logic.soil_analysis import predict_soil_type, predict_npk, calculate_soil_score, soil_suitability_message, predict_salinity
from analysis.logic.crop_rec import get_crop_recommendation
from analysis.logic.fertilizer import recommend_fertilizer
from analysis.logic.main import get_user_input  # Import the input function from main.py

@csrf_exempt  # Disable CSRF protection for this view to allow Arduino data to be sent
def soil_analysis_view(request):
    # Get user input from main.py (Arduino sensor data or default values)
    user_input = get_user_input()  # This will fetch data from Arduino or use default if there's an issue

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

    # Define soil suitability class (for color coding in the front-end)
    soil_suitability_class = 'green' if soil_score > 70 else 'yellow' if soil_score > 40 else 'red'

    # Prepare context data to pass to the template
    context = {
        'soil_type': predicted_soil_type,
        'npk': npk,
        'soil_score': soil_score,
        'soil_suitability': soil_suitability,
        'recommended_crop': recommended_crop,
        'recommended_fertilizer': recommended_fertilizer,
        'soil_suitability_class': soil_suitability_class  # Include this for color coding
    }

    # Render the template with the context data
    return render(request, 'analysis/soil_analysis_output.html', context)

def welcome(request):
    return render(request, 'analysis/welcome.html')

def contact(request):
    return render(request, 'analysis/contact.html')

def start_analysis(request):
    # This seems to be an extra function, you can either use it for an initial page or remove it
    return render(request, 'analysis/soil_analysis_output.html')