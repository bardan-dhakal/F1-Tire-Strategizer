import pickle
import pandas as pd
import numpy as np

print("="*60)
print("F1 TIRE STRATEGY - INTERACTIVE PREDICTION TESTER")
print("="*60)
print()

# Load model and encoders
print("Loading model...")
with open('models/rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

with open('models/feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

print("✓ Model loaded successfully!")
print()

def predict_strategy(tire_data):
    """
    Predict strategy for given tire data
    
    tire_data = {
        'compound': 'soft',
        'lap_number': 18,
        'wear_pattern': 'even',
        'sidewall_deformation': False,
        'tyre_pressure': 20.5,
        'is_graining': False,
        'tyre_temperature': 102,
        'track_temperature': 28
    }
    """
    
    # Create derived features
    compound_life_map = {'soft': 22, 'medium': 32, 'hard': 45, 'intermediate': 15, 'wet': 10}
    expected_life = compound_life_map[tire_data['compound']]
    lap_percentage = tire_data['lap_number'] / expected_life
    temp_differential = tire_data['tyre_temperature'] - tire_data['track_temperature']
    is_pressure_optimal = 19 <= tire_data['tyre_pressure'] <= 21.5
    is_temp_optimal = 95 <= tire_data['tyre_temperature'] <= 115
    
    wear_severity_map = {'even': 0, 'inner': 2, 'outer': 2, 'center': 3, 'uneven': 4}
    wear_severity = wear_severity_map[tire_data['wear_pattern']]
    
    risk_score = (
        lap_percentage * 40 +
        wear_severity * 10 +
        int(tire_data['sidewall_deformation']) * 50 +
        int(tire_data['is_graining']) * 15 +
        int(not is_pressure_optimal) * 10 +
        int(not is_temp_optimal) * 5
    )
    
    # Encode categorical features
    compound_encoded = label_encoders['compound'].transform([tire_data['compound']])[0]
    wear_pattern_encoded = label_encoders['wear_pattern'].transform([tire_data['wear_pattern']])[0]
    
    # Create feature vector
    features = [
        compound_encoded,
        tire_data['lap_number'],
        wear_pattern_encoded,
        int(tire_data['sidewall_deformation']),
        tire_data['tyre_pressure'],
        int(tire_data['is_graining']),
        tire_data['tyre_temperature'],
        tire_data['track_temperature'],
        lap_percentage,
        temp_differential,
        is_pressure_optimal,
        is_temp_optimal,
        wear_severity,
        risk_score
    ]
    
    # Predict
    X = pd.DataFrame([features], columns=feature_columns)
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    
    # Get confidence
    confidence = max(probabilities) * 100
    
    return {
        'strategy': prediction,
        'confidence': confidence,
        'risk_score': risk_score,
        'lap_percentage': lap_percentage * 100
    }

# ============================================
# TEST SCENARIOS
# ============================================

print("="*60)
print("TEST SCENARIOS")
print("="*60)
print()

test_scenarios = [
    {
        'name': '🟢 Perfect Push Conditions',
        'data': {
            'compound': 'soft',
            'lap_number': 8,
            'wear_pattern': 'even',
            'sidewall_deformation': False,
            'tyre_pressure': 20.5,
            'is_graining': False,
            'tyre_temperature': 102,
            'track_temperature': 28
        }
    },
    {
        'name': '🔴 Critical Deformation',
        'data': {
            'compound': 'medium',
            'lap_number': 25,
            'wear_pattern': 'even',
            'sidewall_deformation': True,
            'tyre_pressure': 20.0,
            'is_graining': False,
            'tyre_temperature': 105,
            'track_temperature': 30
        }
    },
    {
        'name': '🟡 Tire Management Mode',
        'data': {
            'compound': 'medium',
            'lap_number': 28,
            'wear_pattern': 'center',
            'sidewall_deformation': False,
            'tyre_pressure': 22.5,
            'is_graining': False,
            'tyre_temperature': 115,
            'track_temperature': 42
        }
    },
    {
        'name': '🔵 Early Stint Graining',
        'data': {
            'compound': 'soft',
            'lap_number': 5,
            'wear_pattern': 'uneven',
            'sidewall_deformation': False,
            'tyre_pressure': 20.0,
            'is_graining': True,
            'tyre_temperature': 88,
            'track_temperature': 16
        }
    },
    {
        'name': '⚪ Normal Monitoring',
        'data': {
            'compound': 'hard',
            'lap_number': 20,
            'wear_pattern': 'even',
            'sidewall_deformation': False,
            'tyre_pressure': 19.8,
            'is_graining': False,
            'tyre_temperature': 108,
            'track_temperature': 32
        }
    }
]

for scenario in test_scenarios:
    print(f"{scenario['name']}")
    print("-" * 60)
    
    data = scenario['data']
    result = predict_strategy(data)
    
    print(f"  Compound: {data['compound'].upper()}")
    print(f"  Lap: {data['lap_number']} ({result['lap_percentage']:.1f}% of expected life)")
    print(f"  Temperature: Tire {data['tyre_temperature']}°C / Track {data['track_temperature']}°C")
    print(f"  Pressure: {data['tyre_pressure']} PSI")
    print(f"  Wear: {data['wear_pattern']}")
    print(f"  Graining: {'Yes' if data['is_graining'] else 'No'}")
    print(f"  Deformation: {'⚠️  YES!' if data['sidewall_deformation'] else 'No'}")
    print()
    print(f"  🎯 STRATEGY: {result['strategy']}")
    print(f"  📊 Confidence: {result['confidence']:.1f}%")
    print(f"  ⚠️  Risk Score: {result['risk_score']:.1f}/100")
    print()

print()
print("="*60)
print("✓ All test scenarios complete!")
print("="*60)
print()
print("Try your own scenario? Edit the test_scenarios list above!")