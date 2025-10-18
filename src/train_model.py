import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle
import os

print("="*60)
print("F1 TIRE STRATEGY - MODEL TRAINING")
print("="*60)
print()

# ============================================
# 1. LOAD DATA
# ============================================

print("Loading data...")
df = pd.read_csv('../data/generated/f1_tire_data.csv')
edge_df = pd.read_csv('../data/generated/edge_cases.csv')
print(f"✓ Loaded {len(df)} training samples")
print(f"✓ Loaded {len(edge_df)} edge cases")
print()

# ============================================
# 2. PREPARE FEATURES
# ============================================

print("Preparing features...")

# Encode categorical variables
label_encoders = {}

# Encode compound
le_compound = LabelEncoder()
df['compound_encoded'] = le_compound.fit_transform(df['compound'])
label_encoders['compound'] = le_compound

# Encode wear pattern
le_wear = LabelEncoder()
df['wear_pattern_encoded'] = le_wear.fit_transform(df['wear_pattern'])
label_encoders['wear_pattern'] = le_wear

# Convert boolean to int
df['sidewall_deformation_int'] = df['sidewall_deformation'].astype(int)
df['is_graining_int'] = df['is_graining'].astype(int)

# Select features for modeling
feature_columns = [
    'compound_encoded',
    'lap_number',
    'wear_pattern_encoded',
    'sidewall_deformation_int',
    'tyre_pressure',
    'is_graining_int',
    'tyre_temperature',
    'track_temperature',
    'lap_percentage',
    'temp_differential',
    'is_pressure_optimal',
    'is_temp_optimal',
    'wear_severity',
    'risk_score'
]

X = df[feature_columns]
y = df['strategy']

print(f"✓ Features prepared: {len(feature_columns)} features")
print(f"  Features: {feature_columns}")
print()

# ============================================
# 3. SPLIT DATA
# ============================================

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✓ Training set: {len(X_train)} samples")
print(f"✓ Test set: {len(X_test)} samples")
print()

# ============================================
# 4. TRAIN DECISION TREE
# ============================================

print("="*60)
print("TRAINING DECISION TREE")
print("="*60)
print()

dt_model = DecisionTreeClassifier(
    max_depth=10,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42
)

print("Training Decision Tree...")
dt_model.fit(X_train, y_train)
print("✓ Training complete!")
print()

# Evaluate
y_pred_dt = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, y_pred_dt)

print(f"Decision Tree Accuracy: {dt_accuracy*100:.2f}%")
print()
print("Classification Report:")
print(classification_report(y_test, y_pred_dt))

# Feature importance
feature_importance_dt = pd.DataFrame({
    'feature': feature_columns,
    'importance': dt_model.feature_importances_
}).sort_values('importance', ascending=False)

print("Top 5 Most Important Features:")
print(feature_importance_dt.head())
print()

# ============================================
# 5. TRAIN RANDOM FOREST
# ============================================

print("="*60)
print("TRAINING RANDOM FOREST")
print("="*60)
print()

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

print("Training Random Forest (this may take 30-60 seconds)...")
rf_model.fit(X_train, y_train)
print("✓ Training complete!")
print()

# Evaluate
y_pred_rf = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, y_pred_rf)

print(f"Random Forest Accuracy: {rf_accuracy*100:.2f}%")
print()
print("Classification Report:")
print(classification_report(y_test, y_pred_rf))

# Feature importance
feature_importance_rf = pd.DataFrame({
    'feature': feature_columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("Top 5 Most Important Features:")
print(feature_importance_rf.head())
print()

# ============================================
# 6. TEST ON EDGE CASES
# ============================================

print("="*60)
print("TESTING ON EDGE CASES")
print("="*60)
print()

# Prepare edge case features
edge_df['compound_encoded'] = le_compound.transform(edge_df['compound'])
edge_df['wear_pattern_encoded'] = le_wear.transform(edge_df['wear_pattern'])
edge_df['sidewall_deformation_int'] = edge_df['sidewall_deformation'].astype(int)
edge_df['is_graining_int'] = edge_df['is_graining'].astype(int)

# Create derived features for edge cases
compound_life_map = {'soft': 22, 'medium': 32, 'hard': 45, 'intermediate': 15, 'wet': 10}
edge_df['expected_life'] = edge_df['compound'].map(compound_life_map)
edge_df['lap_percentage'] = edge_df['lap_number'] / edge_df['expected_life']
edge_df['temp_differential'] = edge_df['tyre_temperature'] - edge_df['track_temperature']
edge_df['is_pressure_optimal'] = edge_df['tyre_pressure'].between(19, 21.5)
edge_df['is_temp_optimal'] = edge_df['tyre_temperature'].between(95, 115)

wear_severity_map = {'even': 0, 'inner': 2, 'outer': 2, 'center': 3, 'uneven': 4}
edge_df['wear_severity'] = edge_df['wear_pattern'].map(wear_severity_map)

edge_df['risk_score'] = (
    edge_df['lap_percentage'] * 40 +
    edge_df['wear_severity'] * 10 +
    edge_df['sidewall_deformation_int'] * 50 +
    edge_df['is_graining_int'] * 15 +
    (~edge_df['is_pressure_optimal']).astype(int) * 10 +
    (~edge_df['is_temp_optimal']).astype(int) * 5
)

X_edge = edge_df[feature_columns]
y_edge_true = edge_df['strategy']

# Predict with Random Forest (better model)
y_edge_pred = rf_model.predict(X_edge)

# Show results
print("Edge Case Predictions:")
print("-" * 80)
results = pd.DataFrame({
    'Scenario': edge_df['scenario_name'].values if 'scenario_name' in edge_df.columns else [f"Case {i+1}" for i in range(len(edge_df))],
    'Compound': edge_df['compound'].values,
    'Lap': edge_df['lap_number'].values,
    'Expected': y_edge_true.values,
    'Predicted': y_edge_pred,
    'Match': ['✓' if exp == pred else '✗' for exp, pred in zip(y_edge_true, y_edge_pred)]
})
print(results.to_string(index=False))
print()

edge_accuracy = accuracy_score(y_edge_true, y_edge_pred)
print(f"Edge Case Accuracy: {edge_accuracy*100:.2f}%")
print()

# ============================================
# 7. SAVE MODELS
# ============================================

print("="*60)
print("SAVING MODELS")
print("="*60)
print()

# Create models directory
os.makedirs('../models', exist_ok=True)

# Save Random Forest (best model)
with open('../models/rf_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
print("✓ Saved Random Forest model: models/rf_model.pkl")

# Save Decision Tree
with open('../models/dt_model.pkl', 'wb') as f:
    pickle.dump(dt_model, f)
print("✓ Saved Decision Tree model: models/dt_model.pkl")

# Save label encoders
with open('../models/label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
print("✓ Saved label encoders: models/label_encoders.pkl")

# Save feature names
with open('../models/feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)
print("✓ Saved feature columns: models/feature_columns.pkl")

# Save metadata
metadata = {
    'train_samples': len(X_train),
    'test_samples': len(X_test),
    'dt_accuracy': dt_accuracy,
    'rf_accuracy': rf_accuracy,
    'edge_accuracy': edge_accuracy,
    'feature_count': len(feature_columns),
    'strategies': list(y.unique())
}

with open('../models/metadata.pkl', 'wb') as f:
    pickle.dump(metadata, f)
print("✓ Saved metadata: models/metadata.pkl")

print()
print("="*60)
print("MODEL TRAINING COMPLETE!")
print("="*60)
print()
print(f"✓ Decision Tree Accuracy: {dt_accuracy*100:.2f}%")
print(f"✓ Random Forest Accuracy: {rf_accuracy*100:.2f}%")
print(f"✓ Edge Case Accuracy: {edge_accuracy*100:.2f}%")
print()
print("Models saved to: models/")
print()
print("Next steps:")
print("1. Test predictions: python src/test_predictions.py")
print("2. Build API: python src/api.py")
print("3. Create dashboard: frontend/")