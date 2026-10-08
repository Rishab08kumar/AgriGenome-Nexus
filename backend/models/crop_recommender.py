import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# ── 175 REAL ICAR VARIETIES from flower_ml_training_dataset.xlsx ──
# Source: ICAR-IARI cultivar list, PAU, IIHR Arka series, Agmarknet
FLOWER_DATA = [
    # (crop, variety, cultivar_group, N_opt, P_opt, K_opt, pH_opt, EC_opt, temp_opt, hum_opt, moist_opt)
    ("Rose","Abhisarika","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Anurag","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Arjun","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Arka Parimala","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Aruna","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Ashwini","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Bhim","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Century Two seedling","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Chambe di Kali","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Chitra","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Dil-Ki-Rani","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Dr. B.P. Pal","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Dr. Benjamin Pal","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Dr. Bharat Ram","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Dr. M.S. Randhawa","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Dr. R.R. Pal","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Dulhan","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Eiffel tower X Queen Elizabeth","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Ganga","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Golden Afternoon","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Haseena","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Homage","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Jawani","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Lalima","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Lal Makhmal","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Madhosh","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Maharani","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Mother Teresa","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Mridula","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Mrinalini","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Mrs. K. B. Sharma","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Nayika","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Nehru centenary","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Nurjahan","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pink Montezuma","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Preyasi","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Priyadharshini","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Ajay","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Arun","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Bahadur","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Garima","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Mansij","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Mohit","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Priya","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Sonara","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Raja Ram Mohan Roy","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Raja S.S. Nalagarh","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Rajkumari","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Raktagandha","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Raktima","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Ranjana","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Ratnaar","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Sahasradhara","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Shanti Pal","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Shreyasi","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Sir C. V. Raman","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Soma","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Sugandha","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Surabhi","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Surekha","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Surkhab","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Jawahar","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Shiloz Mukherjee","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Indian Princess","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Gaurav","Hybrid Tea",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Shatabdi","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Akash Sundari","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Delhi white Powder Puff","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Delhi Pink Powder Puff","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Anitha","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Arunima","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Banjaran","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Chingari","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Deepak","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Delhi Brightness","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Delhi Princess","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Dr. S. S. Bhatnagar","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Himangini","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Jantar Mantar","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Krishna","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Lahar","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Loree","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Madhura","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Manmatha","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Manasi","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Mohini","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Navneet","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Neelambari","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Prema","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Punchu","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Abhishek","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Barahmasi","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Komal","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Pitambar","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Rupali","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Sabnam","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Sadabahar","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Shola","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Sindhoor","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Suchitra","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Surdas","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Suryakiran","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Suryodaya","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Tarang","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Virangana","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Manhar","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Urmil","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Pusa Muskan","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Rose","Rose Sherbet","Floribunda",160,35,175,6.3,1.25,25,70,45),
    ("Marigold","Pusa Narangi Gainda","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Pusa Basanti Gainda","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Pusa Arpita","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Pusa Bahar","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Pusa Deep","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","African Yellow","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","African Orange","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","French Yellow","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","French Orange","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Arka Bangara","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Arka Agni","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Arka Bhanu","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Arka Abhi","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Arka Bhagirath","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Marigold","Arka Anmol","Marigold",150,35,170,6.5,1.2,24,65,45),
    ("Jasmine","Maid of Orleans","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Belle of India","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Arabian Nights","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Gundumalli","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Rambha","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Mysore Mallige","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Arka Aradhana","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Arka Surabhi","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Arka Amogh","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Parimullai","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Pitchi","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Jasmine","Jathi Mallige","Jasmine",140,35,150,6.5,1.1,26,65,45),
    ("Chrysanthemum","Arka Ravi","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Arka Swarna","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Arka Kirti","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Arka Keshav","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Arka Shanti","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Arka Chandrika","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Arka Ganga","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Arka Kesari","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Arka Pink Star","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Pusa Aditya","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Pusa Centenary","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Pusa Anmol","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Pusa Sona","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Pusa Chitraksha","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Chrysanthemum","Pusa Guldaudi","Chrysanthemum",160,45,200,6.3,1.3,22,65,45),
    ("Dianthus","Telstar","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Super Trouper","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Ideal","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Diana","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Amazon","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Corona","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Parfait","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Sunflor","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Sweet","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Jolt","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Rockin","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Dianthus","Dianthus Diabunda","Dianthus",135,35,170,6.5,1.2,20,60,40),
    ("Hibiscus","Arka Amulya","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Arka Shubha","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Arka Prabhath","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Arka Savitri","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Arka Bindu","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Arka Harsha","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","President","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Brilliant","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Double Red","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Yellow","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Pink Versicolor","Hibiscus",160,45,200,6.5,1.3,26,70,50),
    ("Hibiscus","Cooperi","Hibiscus",160,45,200,6.5,1.3,26,70,50),
]

# ── VARIETY → TOP 3 RECOMMENDATIONS LOOKUP ───────────────────────
# For each species, list the most commercially important varieties
TOP_VARIETIES = {
    "Rose":          ["Pusa Gaurav","Arunima","Arka Parimala","Pusa Priya","Sadabahar"],
    "Marigold":      ["Pusa Narangi Gainda","Arka Agni","Arka Bhanu","African Orange","Pusa Basanti Gainda"],
    "Jasmine":       ["Mysore Mallige","Arka Aradhana","Gundumalli","Belle of India","Arka Surabhi"],
    "Chrysanthemum": ["Arka Ravi","Pusa Sona","Arka Swarna","Pusa Guldaudi","Arka Kirti"],
    "Dianthus":      ["Telstar","Dianthus Ideal","Dianthus Amazon","Dianthus Super Trouper","Dianthus Diana"],
    "Hibiscus":      ["Arka Amulya","President","Arka Shubha","Brilliant","Arka Savitri"],
}

CULTIVAR_GROUP = {row[1]: row[2] for row in FLOWER_DATA}


def _build_training_data():
    rows, labels = [], []
    np.random.seed(42)
    for (crop, variety, group, N, P, K, ph, ec, temp, hum, moist) in FLOWER_DATA:
        for _ in range(100):
            rows.append({
                'N':             N    * np.random.uniform(0.85, 1.15),
                'P':             P    * np.random.uniform(0.85, 1.15),
                'K':             K    * np.random.uniform(0.85, 1.15),
                'ph':            ph   * np.random.uniform(0.97, 1.03) if np.random.rand() > 0.15 else np.nan,
                'ec':            ec   * np.random.uniform(0.85, 1.15),
                'temperature':   temp * np.random.uniform(0.90, 1.10),
                'humidity':      hum  * np.random.uniform(0.90, 1.10),
                'soil_moisture': moist* np.random.uniform(0.90, 1.10),
            })
            labels.append(crop)   # predict SPECIES (Rose/Marigold/etc.)
    return pd.DataFrame(rows), pd.Series(labels)


class CropRecommender:
    def __init__(self):
        self.model   = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
        self.imputer = SimpleImputer(strategy='mean')
        self._train()

    def _train(self):
        print("🌸 Training floriculture recommender (175 ICAR varieties)...")
        X, y = _build_training_data()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        self.imputer.fit(X_train)
        self.model.fit(self.imputer.transform(X_train), y_train)
        acc = accuracy_score(y_test, self.model.predict(self.imputer.transform(X_test)))
        print(f"✅ Model ready — Accuracy: {acc*100:.1f}% | Varieties: {len(FLOWER_DATA)} | Species: 6")

    def predict(self, input_dict):
        features = pd.DataFrame([{
            'N':             input_dict.get('N',             0.0),
            'P':             input_dict.get('P',             0.0),
            'K':             input_dict.get('K',             0.0),
            'ph':            input_dict.get('ph',            np.nan),
            'ec':            input_dict.get('ec',            0.0),
            'temperature':   input_dict.get('temperature',   0.0),
            'humidity':      input_dict.get('humidity',      0.0),
            'soil_moisture': input_dict.get('soil_moisture', 0.0),
        }])

        X       = self.imputer.transform(features)
        probs   = self.model.predict_proba(X)[0]
        top3_idx = np.argsort(probs)[::-1][:3]

        results = []
        for idx in top3_idx:
            species = self.model.classes_[idx]
            top_vars = TOP_VARIETIES.get(species, [])
            results.append({
                "rank":              len(results) + 1,
                "flower_species":    species,
                "confidence":        round(float(probs[idx]) * 100, 1),
                "recommended_varieties": top_vars[:3],
                "cultivar_group":    CULTIVAR_GROUP.get(top_vars[0], "—") if top_vars else "—",
                "total_varieties":   sum(1 for r in FLOWER_DATA if r[0] == species),
                "genomic_strain":    f"{species} - ICAR Certified Cultivar",
            })

        return {
            "best_recommendation": results[0],
            "alternatives":        results[1:],
            "ph_status":           "sensor connected" if input_dict.get('ph') else "sensor not connected - auto filled",
            "dataset_source":      "ICAR-IARI / PAU / IIHR Arka Series — 175 certified varieties"
        }


recommender = CropRecommender()