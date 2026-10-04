import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

class CropRecommender:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.imputer = SimpleImputer(strategy='mean')
        self.crops = [
            "Rice IR64", "Wheat HD-2967", "Tomato H-86", "Cotton MCU-5", 
            "Maize DHM-117", "Soybean JS-335", "Groundnut TAG-24", 
            "Sugarcane CO-86032", "Banana Grand Naine", "Pepper Panniyur-1"
        ]
        self.strains = [
            "Drought-resilient Rice IR64", "High-yield Wheat HD-2967", 
            "High-yield Tomato H-86", "Bt Cotton MCU-5", "Hybrid Maize DHM-117", 
            "High-protein Soybean JS-335", "High-oil Groundnut TAG-24", 
            "High-sucrose Sugarcane CO-86032", "Disease-resistant Banana Grand Naine", 
            "High-pungency Pepper Panniyur-1"
        ]
        self.is_trained = False
        self.train()

    def generate_synthetic_data(self):
        np.random.seed(42)
        n_samples = 300
        X = {
            'latitude': np.random.uniform(8.0, 37.0, n_samples),
            'longitude': np.random.uniform(68.0, 97.0, n_samples),
            'soil_moisture': np.random.uniform(10, 90, n_samples),
            'temperature': np.random.uniform(15, 40, n_samples),
            'humidity': np.random.uniform(30, 90, n_samples),
            'N': np.random.uniform(0, 100, n_samples),
            'P': np.random.uniform(0, 100, n_samples),
            'K': np.random.uniform(0, 100, n_samples),
            'ec': np.random.uniform(0.1, 2.5, n_samples),
            'ph': np.random.uniform(4.5, 8.5, n_samples)
        }
        # Add some NaNs to pH
        nan_indices = np.random.choice(n_samples, size=30, replace=False)
        X['ph'][nan_indices] = np.nan
        
        y = np.random.choice(self.crops, n_samples)
        
        df = pd.DataFrame(X)
        return df, y

    def train(self):
        X_df, y = self.generate_synthetic_data()
        X_imputed = self.imputer.fit_transform(X_df)
        self.model.fit(X_imputed, y)
        self.is_trained = True

    def predict(self, input_dict):
        if not self.is_trained:
            self.train()
        
        # Features: latitude, longitude, soil_moisture, temperature, humidity, N, P, K, ec, ph
        ph_val = input_dict.get('ph')
        if ph_val is None:
            ph_val = np.nan
            
        features = [
            input_dict.get('latitude', 0.0),
            input_dict.get('longitude', 0.0),
            input_dict.get('soil_moisture', 0.0),
            input_dict.get('temperature', 0.0),
            input_dict.get('humidity', 0.0),
            input_dict.get('nitrogen', 0.0),
            input_dict.get('phosphorus', 0.0),
            input_dict.get('potassium', 0.0),
            input_dict.get('ec', 0.0),
            ph_val
        ]
        
        X_test = pd.DataFrame([features], columns=[
            'latitude', 'longitude', 'soil_moisture', 'temperature', 
            'humidity', 'N', 'P', 'K', 'ec', 'ph'
        ])
        X_imputed = self.imputer.transform(X_test)
        
        probs = self.model.predict_proba(X_imputed)[0]
        max_idx = np.argmax(probs)
        pred_class = self.model.classes_[max_idx]
        confidence = probs[max_idx]
        
        idx = self.crops.index(pred_class)
        strain = self.strains[idx]
        
        return {
            "crop_variety": pred_class,
            "genomic_strain": strain,
            "confidence": float(confidence)
        }

recommender = CropRecommender()
