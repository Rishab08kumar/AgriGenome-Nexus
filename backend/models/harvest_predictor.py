import math

class HarvestPredictor:
    def __init__(self):
        # ── FLOWER HARVEST DAYS (days from planting to first harvest) ─
        self.CROP_MATURITY_DAYS = {
            "Rose":          75,
            "Marigold":      60,
            "Jasmine":       90,
            "Gerbera":       90,
            "Chrysanthemum": 100,
            "Lotus":         80,
            "Sunflower":     70,
            "Tuberose":      120,
            "Gladiolus":     90,
            "Anthurium":     120,
            "Hibiscus":      60,
        }

    def predict(self, input_dict):
        crop = input_dict.get('crop_variety', 'Rose')

        # Match variety name to species
        matched = "Rose"
        for species in self.CROP_MATURITY_DAYS.keys():
            if species.lower() in crop.lower():
                matched = species
                break

        expected_days = self.CROP_MATURITY_DAYS[matched]
        days_passed   = input_dict.get('days_since_planting', 0)

        # Sigmoid maturity curve
        midpoint = expected_days * 0.8
        k        = 0.1
        maturity = 100.0 / (1 + math.exp(-k * (days_passed - midpoint)))

        days_to_harvest = max(0, expected_days - days_passed)
        alert           = maturity > 90.0

        return {
            "maturity_score":   round(maturity, 2),
            "days_to_harvest":  days_to_harvest,
            "alert":            alert,
            "flower_species":   matched,
            "message": "🌸 Harvest window approaching! Ready to cut." if alert else "🌱 Crop is still growing."
        }


predictor = HarvestPredictor()