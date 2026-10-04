import numpy as np
import pandas as pd
import xgboost as xgb

class MarketForecaster:
    def __init__(self):
        self.model = xgb.XGBRegressor(objective='reg:squarederror')
        self.regions = ["Punjab", "Maharashtra", "Karnataka", "UP", "MP", "Gujarat", "AP", "Tamil Nadu"]
        self.seasons = ["Kharif", "Rabi", "Zaid"]
        self.grades = ["A", "B", "C"]
        self.is_trained = False
        self.train()

    def generate_synthetic_data(self):
        np.random.seed(42)
        n = 500
        X = pd.DataFrame({
            'crop_idx': np.random.randint(0, 10, n),
            'region_idx': np.random.randint(0, len(self.regions), n),
            'season_idx': np.random.randint(0, len(self.seasons), n),
            'grade_idx': np.random.randint(0, len(self.grades), n)
        })
        y = 1000 + (X['crop_idx'] * 200) + (X['grade_idx'] * -100) + np.random.normal(0, 100, n)
        return X, y

    def train(self):
        X, y = self.generate_synthetic_data()
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, input_dict):
        crop_idx = hash(input_dict.get('crop_variety', '')) % 10
        region_idx = self.regions.index(input_dict.get('region', self.regions[0])) if input_dict.get('region') in self.regions else 0
        season_idx = self.seasons.index(input_dict.get('season', self.seasons[0])) if input_dict.get('season') in self.seasons else 0
        grade_idx = self.grades.index(input_dict.get('yield_grade', 'A')) if input_dict.get('yield_grade') in self.grades else 0
        
        X_test = pd.DataFrame([[crop_idx, region_idx, season_idx, grade_idx]], 
                              columns=['crop_idx', 'region_idx', 'season_idx', 'grade_idx'])
                              
        pred = self.model.predict(X_test)[0]
        
        return {
            "predicted_price": float(pred),
            "price_range_low": float(pred * 0.9),
            "price_range_high": float(pred * 1.1),
            "currency": "INR",
            "unit": "per quintal"
        }

forecaster = MarketForecaster()
