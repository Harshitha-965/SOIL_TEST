from django.db import models

class SoilAnalysis(models.Model):
    soil_type = models.CharField(max_length=255)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    soil_score = models.FloatField(blank=True, null=True)  # Auto-calculated field

    def calculate_soil_score(self):
        """Calculate the soil score based on nutrient levels."""
        # Example calculation logic (replace with your formula if different)
        return (self.nitrogen + self.phosphorus + self.potassium) / 3

    def save(self, *args, **kwargs):
        """Override the save method to calculate soil_score before saving."""
        self.soil_score = self.calculate_soil_score()
        super().save(*args, **kwargs)

    def str(self):
        return f"Soil Analysis: {self.soil_type} (Score: {self.soil_score:.2f})"


class CropRecommendation(models.Model):
    soil_type = models.CharField(max_length=255)
    recommended_crop = models.CharField(max_length=255)

    def str(self):
        return f"Recommended Crop for {self.soil_type}: {self.recommended_crop}"


class FertilizerRecommendation(models.Model):
    soil_type = models.CharField(max_length=255)
    recommended_fertilizer = models.CharField(max_length=255)

    def str(self):
        return f"Recommended Fertilizer for {self.soil_type}: {self.recommended_fertilizer}"