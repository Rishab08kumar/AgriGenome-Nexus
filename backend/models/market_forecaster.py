import numpy as np
import pandas as pd
import xgboost as xgb

class MarketForecaster:
    def __init__(self):
        self.model   = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
        self.regions = ["Karnataka", "Tamil Nadu", "Maharashtra", "Punjab", "UP", "Gujarat", "AP", "MP"]
        self.seasons = ["Kharif", "Rabi", "Zaid"]
        self.grades  = ["A", "B", "C"]

        # Base APMC prices per flower (₹/quintal) — from Agmarknet averages
        self.FLOWER_BASE_PRICES = {
            "Rose":          8000,
            "Marigold":      2000,
            "Jasmine":       12000,
            "Gerbera":       6000,
            "Chrysanthemum": 4000,
            "Lotus":         5000,
            "Sunflower":     2500,
            "Tuberose":      7000,
            "Gladiolus":     5000,
            "Anthurium":     15000,
            "Hibiscus":      3000,
        }
        self.flower_names = list(self.FLOWER_BASE_PRICES.keys())
        self._train()

    def _get_base_price(self, crop_variety):
        for flower in self.FLOWER_BASE_PRICES:
            if flower.lower() in crop_variety.lower():
                return self.FLOWER_BASE_PRICES[flower], self.flower_names.index(flower)
        return 4000, 0  # default

    def _train(self):
        np.random.seed(42)
        n = 1000
        rows, prices = [], []
        for _ in range(n):
            flower_idx  = np.random.randint(0, len(self.flower_names))
            region_idx  = np.random.randint(0, len(self.regions))
            season_idx  = np.random.randint(0, len(self.seasons))
            grade_idx   = np.random.randint(0, len(self.grades))
            base_price  = list(self.FLOWER_BASE_PRICES.values())[flower_idx]
            grade_mult  = [1.15, 1.0, 0.82][grade_idx]
            region_mult = [1.1, 1.05, 1.0, 0.95, 0.9, 1.02, 1.0, 0.95][region_idx]
            price = base_price * grade_mult * region_mult + np.random.normal(0, 200)
            rows.append([flower_idx, region_idx, season_idx, grade_idx])
            prices.append(price)

        X = pd.DataFrame(rows, columns=['flower_idx','region_idx','season_idx','grade_idx'])
        self.model.fit(X, prices)

    def predict(self, input_dict):
        base_price, flower_idx = self._get_base_price(input_dict.get('crop_variety', 'Rose'))
        region_idx  = self.regions.index(input_dict.get('region', 'Karnataka')) if input_dict.get('region') in self.regions else 0
        season_idx  = self.seasons.index(input_dict.get('season', 'Rabi'))      if input_dict.get('season')  in self.seasons else 0
        grade_idx   = self.grades.index(input_dict.get('yield_grade', 'A'))     if input_dict.get('yield_grade') in self.grades else 0

        X_test = pd.DataFrame(
            [[flower_idx, region_idx, season_idx, grade_idx]],
            columns=['flower_idx','region_idx','season_idx','grade_idx']
        )
        pred = float(self.model.predict(X_test)[0])

        return {
            "predicted_price":  round(pred, 2),
            "price_range_low":  round(pred * 0.90, 2),
            "price_range_high": round(pred * 1.10, 2),
            "currency":         "INR",
            "unit":             "per quintal",
            "fair_price_alert": pred < (base_price * 0.85)
        }


forecaster = MarketForecaster()