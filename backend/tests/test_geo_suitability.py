from types import SimpleNamespace
from models.geo_crop_suitability import evaluate

def test_geo_ranking():
    data = SimpleNamespace(latitude=12.97, longitude=77.59, planting_month=7, temperature=28, humidity=70,
        soil_moisture=58, nitrogen=150, phosphorus=55, potassium=185, ec=1.5, soil_ph=6.8,
        annual_rainfall_mm=900, top_k=4)
    result = evaluate(data)
    assert len(result['recommendations']) == 4
    assert all(0 <= crop['score'] <= 100 for crop in result['recommendations'])
    assert result['recommendations'] == sorted(result['recommendations'], key=lambda crop: crop['score'], reverse=True)
    assert result['data_quality'].startswith('Prototype')
