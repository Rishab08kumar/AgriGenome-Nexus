import math

class HarvestPredictor:
    def __init__(self):
        self.CROP_MATURITY_DAYS = {
            "Rice": 120, "Wheat": 110, "Tomato": 75, "Cotton": 180, 
            "Maize": 95, "Soybean": 100, "Groundnut": 120, "Sugarcane": 365, 
            "Banana": 270, "Pepper": 180
        }

    def predict(self, input_dict):
        crop = input_dict.get('crop_variety', 'Rice')
        base_crop = "Rice"
        for k in self.CROP_MATURITY_DAYS.keys():
            if k.lower() in crop.lower():
                base_crop = k
                break
                
        expected_days = self.CROP_MATURITY_DAYS[base_crop]
        days_passed = input_dict.get('days_since_planting', 0)
        
        midpoint = expected_days * 0.8
        k = 0.1
        maturity = 100.0 / (1 + math.exp(-k * (days_passed - midpoint)))
        
        days_to_harvest = max(0, expected_days - days_passed)
        alert = maturity > 90.0
        
        return {
            "maturity_score": round(maturity, 2),
            "days_to_harvest": days_to_harvest,
            "alert": alert,
            "message": "Harvest window approaching!" if alert else "Crop is still growing."
        }

predictor = HarvestPredictor()
