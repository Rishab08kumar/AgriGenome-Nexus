import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Floriculture varieties mapped to genomic cultivar tags
flowers_data = [
    # Temp(C), Humidity(%), Moisture(%), Light(lux), EC, pH, Crop, Strain
    [22, 65, 60, 45000, 1.2, 6.2, "Rose", "Rosa hybrida - Dutch Red"],
    [28, 50, 40, 60000, 1.0, 6.8, "Marigold", "Tagetes erecta - African Gold"],
    [30, 75, 70, 50000, 1.5, 6.5, "Jasmine", "Jasminum sambac - Mysuru Mallige"],
    [20, 60, 50, 35000, 1.1, 6.0, "Chrysanthemum", "Chrysanthemum indicum - Yellow Gem"],
    [25, 70, 65, 40000, 1.3, 6.4, "Hibiscus", "Hibiscus rosa-sinensis - Tropica"],
]

# Expand into dataset with variations
import numpy as np
np.random.seed(42)
expanded = []
for _ in range(500):
    base = flowers_data[np.random.choice(len(flowers_data))]
    expanded.append([
        base[0] + np.random.uniform(-3, 3), # Temp
        base[1] + np.random.uniform(-10, 10), # Humidity
        base[2] + np.random.uniform(-10, 10), # Moisture
        base[3] + np.random.uniform(-5000, 5000), # Light
        base[4] + np.random.uniform(-0.2, 0.2), # EC
        base[5] + np.random.uniform(-0.5, 0.5) if np.random.rand() > 0.15 else np.nan, # pH
        base[6], # Crop
        base[7] # Strain
    ])

df = pd.DataFrame(expanded, columns=["temperature", "humidity", "soil_moisture", "light_intensity", "ec", "ph", "crop", "genomic_strain"])

X = df[["temperature", "humidity", "soil_moisture", "light_intensity", "ec", "ph"]]
y = df["genomic_strain"]

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

pipeline.fit(X, y)

output_dir = os.path.join(os.path.dirname(__file__), "..", "backend", "models")
os.makedirs(output_dir, exist_ok=True)
joblib.dump(pipeline, os.path.join(output_dir, "crop_recommender.joblib"))
print("🌸 Flower Crop Recommender trained & saved successfully!")