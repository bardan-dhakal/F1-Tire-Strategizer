import pickle
import pandas as pd
import numpy as np
import random

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

def reverse_engineer_meta_data(data, lap_number):
    """
    Reverse engineer realistic sensor data from visual observations
    
    Args:
        data: Dict from Gemini with:
            - color
            - compound  
            - wear_pattern
            - sidewall_deformation
            - is_graining
        lap_number: Current lap number
    
    Returns:
        Dict with:
            - tyre_pressure
            - tyre_temperature
            - track_temperature
    """
    
    compound = data['compound']
    wear_pattern = data['wear_pattern']
    is_graining = data['is_graining']
    sidewall_deformation = data['sidewall_deformation']

    
    # Compound choice gives clues about track conditions
    if compound == 'soft':
        # Teams choose soft on cooler days or for short stints
        track_temp_base = random.uniform(20, 32)
    elif compound == 'medium':
        # Medium works in most conditions
        track_temp_base = random.uniform(25, 38)
    elif compound == 'hard':
        # Hard chosen for hot conditions
        track_temp_base = random.uniform(32, 45)
    elif compound == 'intermediate':
        # Damp/wet conditions
        track_temp_base = random.uniform(12, 25)
    elif compound == 'wet':
        # Heavy rain
        track_temp_base = random.uniform(10, 20)
    else:
        track_temp_base = 28  # Default
    
    # Add some natural variation
    track_temperature = int(track_temp_base + random.uniform(-2, 2))

    # Base tire temp on compound optimal range
    compound_optimal_temps = {
        'soft': (95, 105),
        'medium': (100, 110),
        'hard': (105, 115),
        'intermediate': (85, 95),
        'wet': (75, 85)
    }
    
    optimal_min, optimal_max = compound_optimal_temps.get(
        compound, (100, 110)
    )
    
    # Adjust based on graining
    if is_graining:
        # Graining = tire too cold
        # Temperature below optimal range
        tyre_temp = optimal_min - random.uniform(5, 15)
    else:
        # No graining = tire at or above optimal temp
        # Check wear pattern for more clues
        
        if wear_pattern == 'even':
            # Perfect conditions - in optimal range
            tyre_temp = random.uniform(optimal_min, optimal_max)
        
        elif wear_pattern == 'center':
            # Center wear = overheating
            tyre_temp = optimal_max + random.uniform(5, 15)
        
        elif wear_pattern in ['inner', 'outer']:
            # Edge wear = some overheating + setup issues
            tyre_temp = random.uniform(optimal_min + 5, optimal_max + 10)
        
        elif wear_pattern == 'uneven':
            # Uneven = inconsistent temps
            tyre_temp = random.uniform(optimal_min - 5, optimal_max + 15)
        
        else:
            # Default to optimal range
            tyre_temp = random.uniform(optimal_min, optimal_max)
    
    # Lap wear effect: tires get hotter as they wear
    # Estimate wear percentage based on compound life
    compound_life = {'soft': 22, 'medium': 32, 'hard': 45, 
                     'intermediate': 15, 'wet': 10}
    expected_life = compound_life.get(compound, 30)
    wear_percentage = lap_number / expected_life
    
    # Add heat from wear (up to +10°C for worn tires)
    wear_heat_increase = min(wear_percentage * 10, 10)
    tyre_temp += wear_heat_increase
    
    # Sidewall deformation indicates extreme conditions
    if sidewall_deformation:
        # Either very hot or pressure issue
        tyre_temp = max(tyre_temp, optimal_max + 15)
    
    tyre_temperature = int(tyre_temp)
    

    
    # Base pressure range (normal operating)
    base_pressure_range = (19.0, 21.5)
    
    # Adjust based on wear pattern
    if wear_pattern == 'even':
        # Even wear = optimal pressure
        tyre_pressure = random.uniform(19.5, 21.0)
    
    elif wear_pattern == 'center':
        # Center wear = over-inflated
        tyre_pressure = random.uniform(21.5, 23.5)
    
    elif wear_pattern == 'inner':
        # Inner wear = could be setup or pressure
        tyre_pressure = random.uniform(18.5, 21.5)
    
    elif wear_pattern == 'outer':
        # Outer wear = could be setup or pressure
        tyre_pressure = random.uniform(18.5, 21.5)
    
    elif wear_pattern == 'uneven':
        # Uneven = inconsistent pressure
        tyre_pressure = random.uniform(18.0, 22.5)
    
    else:
        tyre_pressure = random.uniform(19.0, 21.5)
    
    # Sidewall deformation = pressure problem
    if sidewall_deformation:
        # Either very low or very high
        if random.random() < 0.7:  # Usually low pressure
            tyre_pressure = random.uniform(15.0, 17.5)
        else:  # Sometimes over-pressure + heat
            tyre_pressure = random.uniform(23.0, 25.0)
    
    # Temperature affects pressure (physics)
    # Hot tires have higher pressure
    temp_pressure_effect = (tyre_temperature - 100) * 0.05
    tyre_pressure += temp_pressure_effect
    
    # Round to 1 decimal
    tyre_pressure = round(tyre_pressure, 1)
    
    # Clamp to reasonable bounds
    tyre_pressure = max(15.0, min(tyre_pressure, 25.0))

    data.update({
            
        "lap_number": lap_number,
        "tyre_pressure": tyre_pressure,
        "tyre_temperature": tyre_temperature,
        "track_temperature": track_temperature
        })
    
    return data
    