import numpy as np

class DosingEngine:
    def __init__(self):
        self.CROP_THRESHOLDS = {
            # ── ROSE (109 ICAR varieties share these thresholds) ──
            "Rose":          {"min_moisture": 40, "max_moisture": 60, "min_N": 140, "min_P": 30, "min_K": 150, "min_ec": 0.5, "max_ec": 2.0},
            # ── MARIGOLD ──
            "Marigold":      {"min_moisture": 30, "max_moisture": 55, "min_N": 120, "min_P": 25, "min_K": 120, "min_ec": 0.6, "max_ec": 1.8},
            # ── JASMINE ──
            "Jasmine":       {"min_moisture": 40, "max_moisture": 65, "min_N": 100, "min_P": 25, "min_K": 100, "min_ec": 0.5, "max_ec": 1.8},
            # ── CHRYSANTHEMUM ──
            "Chrysanthemum": {"min_moisture": 35, "max_moisture": 60, "min_N": 120, "min_P": 30, "min_K": 150, "min_ec": 0.7, "max_ec": 2.0},
            # ── DIANTHUS ──
            "Dianthus":      {"min_moisture": 30, "max_moisture": 55, "min_N": 100, "min_P": 25, "min_K": 120, "min_ec": 0.6, "max_ec": 1.8},
            # ── HIBISCUS ──
            "Hibiscus":      {"min_moisture": 40, "max_moisture": 65, "min_N": 120, "min_P": 30, "min_K": 150, "min_ec": 0.6, "max_ec": 2.0},
        }

        self.DEFAULT = {
            "min_moisture": 40, "max_moisture": 60,
            "min_N": 120, "min_P": 30, "min_K": 120,
            "min_ec": 0.5, "max_ec": 2.0
        }

    def _get_thresholds(self, crop_variety: str) -> dict:
        """Match any variety name to its species thresholds."""
        # Direct species match
        for species in self.CROP_THRESHOLDS:
            if species.lower() in crop_variety.lower():
                return self.CROP_THRESHOLDS[species], species
        # Default fallback
        return self.DEFAULT, "Unknown"

    def decide(self, sensor_data: dict, crop_variety: str) -> dict:
        thresholds, matched_species = self._get_thresholds(crop_variety)

        # Read all sensor values
        moisture = sensor_data.get('soil_moisture',   sensor_data.get('moisture', 0.0))
        N        = sensor_data.get('N',               sensor_data.get('nitrogen', 0.0))
        P        = sensor_data.get('P',               sensor_data.get('phosphorus', 0.0))
        K        = sensor_data.get('K',               sensor_data.get('potassium', 0.0))
        ec       = sensor_data.get('ec',              0.0)

        pump_on          = False
        valve_open       = False
        nutrient_dose_ml = 0.0
        reasons          = []
        warnings         = []

        # ── PUMP DECISION ─────────────────────────────────────────
        if moisture < thresholds['min_moisture']:
            pump_on = True
            reasons.append(
                f"Soil moisture {moisture:.1f}% below minimum "
                f"{thresholds['min_moisture']}% for {matched_species}"
            )
        elif moisture > thresholds['max_moisture']:
            warnings.append(
                f"Overwatering risk: moisture {moisture:.1f}% "
                f"above max {thresholds['max_moisture']}%"
            )

        # ── VALVE / NUTRIENT DECISION ─────────────────────────────
        if N < thresholds['min_N']:
            valve_open = True
            dose = round((thresholds['min_N'] - N) * 0.5, 1)
            nutrient_dose_ml += dose
            reasons.append(f"N deficiency ({N:.1f} < {thresholds['min_N']}) → dose {dose}ml")

        if P < thresholds['min_P']:
            valve_open = True
            dose = round((thresholds['min_P'] - P) * 0.3, 1)
            nutrient_dose_ml += dose
            reasons.append(f"P deficiency ({P:.1f} < {thresholds['min_P']}) → dose {dose}ml")

        if K < thresholds['min_K']:
            valve_open = True
            dose = round((thresholds['min_K'] - K) * 0.3, 1)
            nutrient_dose_ml += dose
            reasons.append(f"K deficiency ({K:.1f} < {thresholds['min_K']}) → dose {dose}ml")

        # ── EC WARNING ────────────────────────────────────────────
        if ec > thresholds['max_ec']:
            warnings.append(
                f"EC {ec:.2f} dS/m exceeds max {thresholds['max_ec']} — "
                f"salt burn risk, reduce fertilizer"
            )

        return {
            "pump_on":           pump_on,
            "valve_open":        valve_open,
            "nutrient_dose_ml":  round(nutrient_dose_ml, 1),
            "reasons":           reasons,
            "warnings":          warnings,
            "crop_variety":      crop_variety,
            "matched_species":   matched_species,
            "status":            "active" if (pump_on or valve_open) else "standby"
        }


engine = DosingEngine()