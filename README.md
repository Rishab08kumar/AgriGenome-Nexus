# AgriGenome-Nexus 🌾🧬

**AgriGenome-Nexus** is a full-stack, AI-powered precision agriculture platform designed for smart farming systems. It combines multi-sensor telemetry, genomic strain recommendation, ML-driven fertigation, computer vision plant health diagnostic, harvest maturity forecasting, and APMC market price prediction into an immersive dark-mode 3D web dashboard.

---

## 🏛️ System Architecture

```
Sensors (Moisture, Temp, Humidity, Light, NPK, EC, ESP32-CAM)
                  │
                  ▼ (REST POST /api/sensor-data)
     FastAPI Backend (Port 8000) <───> Firebase Realtime DB & Firestore
                  │
     ┌────────────┼────────────┬────────────┬────────────┐
     ▼            ▼            ▼            ▼            ▼
 Model 1      Model 2      Model 3      Model 4      Model 5
 (Random      (Dosing      (MobileNet/  (Harvest     (APMC Price
  Forest)      Engine)      YOLOv8)      Maturity)    Forecaster)
     │            │            │            │            │
     └────────────┴────────────┼────────────┴────────────┘
                               ▼
            React 3D Dashboard (Port 5173 / 3000)
```

---

## 🚀 Quick Setup Instructions

### Location of Workspace
The full-stack application code is located at:
`C:\Users\Rishab MIsty KS\.gemini\antigravity\scratch\AgriGenome-Nexus`

---

### 1. Backend Setup (FastAPI + ML)

```bash
cd "C:\Users\Rishab MIsty KS\.gemini\antigravity\scratch\AgriGenome-Nexus\backend"

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload --port 8000
```

*Interactive Swagger API documentation is available at http://localhost:8000/docs.*

---

### 2. Frontend Setup (React.js + Tailwind + 3D)

```bash
cd "C:\Users\Rishab MIsty KS\.gemini\antigravity\scratch\AgriGenome-Nexus\frontend"

# Install Node packages
npm install

# Start Vite dev server
npm run dev
```

*Access the interactive 3D dashboard at http://localhost:5173.*

---

### 3. Running Mock Sensor Feed

To simulate continuous real-time IoT hardware feeding telemetry to the platform every 5 seconds:

```bash
cd "C:\Users\Rishab MIsty KS\.gemini\antigravity\scratch\AgriGenome-Nexus"
python scripts/mock_sensor_feed.py
```

---

## 🤖 Machine Learning Models Summary

| Model | Target / Output | Tech Stack | Endpoint |
|---|---|---|---|
| **Model 1 — Crop & Cultivar Recommender** | Best crop variety + genomic strain + confidence % | `RandomForestClassifier` + `SimpleImputer` | `POST /api/recommend-crop` |
| **Model 2 — Dosing & Irrigation Decision** | `pump_on`, `valve_open`, `nutrient_dose_ml`, reasons | Physiological Rules + `XGBClassifier` | `POST /api/dosing-decision` |
| **Model 3 — Plant Health & Disease Detector** | Disease label, confidence, bounding boxes | `MobileNetV2` + `Pillow` image pipeline | `POST /api/plant-health` |
| **Model 4 — Harvest Maturity Predictor** | Maturity %, days to harvest countdown, alert flag | Sigmoid curve + crop growth tables | `POST /api/harvest-readiness` |
| **Model 5 — APMC Fair Price Forecaster** | Predicted ₹/quintal price + min/max band | `XGBRegressor` trained on APMC data | `POST /api/market-price` |

---

## 🎨 UI/UX Highlights

- **pH Sensor Placeholder**: Standardized across all models, API schemas, and UI elements. Form inputs gray out the field with a tooltip (*"pH sensor integration coming soon"*), while telemetry cards display a dashed-border state reading `"Sensor Not Connected"`.
- **3D Canvas & Glassmorphism**: Built with high-performance CSS perspective transforms, neon-glow borders, particle backgrounds, and smooth spring animations via `framer-motion`.
- **Responsive Telemetry & Charts**: Interactive graphs powered by `recharts` and `react-circular-progressbar`.
