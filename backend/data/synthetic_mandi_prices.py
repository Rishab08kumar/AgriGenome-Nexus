import pandas as pd
import random
from datetime import datetime, timedelta
import json
import os

CROPS = ["Rice", "Wheat", "Tomato", "Cotton", "Maize", "Soybean", "Groundnut", "Sugarcane", "Banana", "Pepper"]
REGIONS = ["Punjab", "Maharashtra", "Karnataka", "UP", "MP", "Gujarat", "AP", "Tamil Nadu"]
SEASONS = ["Kharif", "Rabi", "Zaid"]
GRADES = ["A", "B", "C"]

def generate_prices(num_records=500):
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for _ in range(num_records):
        crop = random.choice(CROPS)
        region = random.choice(REGIONS)
        season = random.choice(SEASONS)
        grade = random.choice(GRADES)
        
        # Base price mapping roughly based on Indian markets (INR per Quintal)
        base_prices = {
            "Rice": 2500, "Wheat": 2200, "Tomato": 1500, "Cotton": 6000, 
            "Maize": 2000, "Soybean": 4500, "Groundnut": 5500, 
            "Sugarcane": 300, "Banana": 1200, "Pepper": 35000
        }
        
        base = base_prices[crop]
        
        # Multipliers
        grade_mult = {"A": 1.2, "B": 1.0, "C": 0.8}[grade]
        season_mult = 1.0 + random.uniform(-0.1, 0.2) # Fluctuation
        
        price = round(base * grade_mult * season_mult + random.uniform(-100, 100), 2)
        
        # Random date in last year
        days_offset = random.randint(0, 365)
        date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        
        data.append({
            "date": date,
            "crop": crop,
            "region": region,
            "season": season,
            "grade": grade,
            "price_inr_per_q": max(0, price) # ensure positive
        })
        
    return data

def main():
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    print("Generating synthetic mandi prices...")
    data = generate_prices(600)
    
    df = pd.DataFrame(data)
    
    csv_path = os.path.join(os.path.dirname(__file__), 'mandi_prices.csv')
    json_path = os.path.join(os.path.dirname(__file__), 'mandi_prices.json')
    
    df.to_csv(csv_path, index=False)
    print(f"Saved to {csv_path}")
    
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved to {json_path}")

if __name__ == "__main__":
    main()
