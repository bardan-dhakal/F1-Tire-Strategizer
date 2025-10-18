import pandas as pd
import numpy as np

print("="*60)
print("DATA INSPECTION")
print("="*60)
print()

# Load the data
df = pd.read_csv('../data/generated/f1_tire_data.csv')
edge_df = pd.read_csv('../data/generated/edge_cases.csv')

print(f"✓ Loaded {len(df)} training samples")
print(f"✓ Loaded {len(edge_df)} edge cases")
print()

# Show first few rows
print("="*60)
print("SAMPLE DATA (First 5 rows)")
print("="*60)
print(df.head())
print()

# Show data types
print("="*60)
print("DATA TYPES")
print("="*60)
print(df.dtypes)
print()

# Check for missing values
print("="*60)
print("MISSING VALUES CHECK")
print("="*60)
missing = df.isnull().sum()
if missing.sum() == 0:
    print("✓ No missing values found!")
else:
    print("⚠ Missing values detected:")
    print(missing[missing > 0])
print()

# Strategy distribution
print("="*60)
print("STRATEGY DISTRIBUTION")
print("="*60)
strategy_dist = df['strategy'].value_counts()
print(strategy_dist)
print()
print("Percentages:")
print((strategy_dist / len(df) * 100).round(2))
print()

# Compound distribution
print("="*60)
print("COMPOUND DISTRIBUTION")
print("="*60)
compound_dist = df['compound'].value_counts()
print(compound_dist)
print()

# Some basic statistics
print("="*60)
print("KEY STATISTICS")
print("="*60)
print(f"Average lap number: {df['lap_number'].mean():.1f}")
print(f"Average tire temp: {df['tyre_temperature'].mean():.1f}°C")
print(f"Average track temp: {df['track_temperature'].mean():.1f}°C")
print(f"Average pressure: {df['tyre_pressure'].mean():.2f} PSI")
print(f"Graining occurrences: {df['is_graining'].sum()} ({df['is_graining'].mean()*100:.1f}%)")
print(f"Deformation occurrences: {df['sidewall_deformation'].sum()} ({df['sidewall_deformation'].mean()*100:.1f}%)")
print()

# Sanity checks
print("="*60)
print("SANITY CHECKS")
print("="*60)

# Check 1: Are soft tires living reasonable lives?
soft_laps = df[df['compound'] == 'soft']['lap_number']
print(f"✓ Soft tire laps: min={soft_laps.min()}, max={soft_laps.max()}, avg={soft_laps.mean():.1f}")
if soft_laps.max() > 30:
    print("  ⚠ Warning: Some soft tires lasting unusually long")

# Check 2: Are hard tires living reasonable lives?
hard_laps = df[df['compound'] == 'hard']['lap_number']
print(f"✓ Hard tire laps: min={hard_laps.min()}, max={hard_laps.max()}, avg={hard_laps.mean():.1f}")

# Check 3: Temperature relationships
temp_diff = df['tyre_temperature'] - df['track_temperature']
print(f"✓ Tire-Track temp difference: min={temp_diff.min():.1f}, max={temp_diff.max():.1f}, avg={temp_diff.mean():.1f}")
if temp_diff.min() < 0:
    print("  ⚠ Warning: Some tires cooler than track (unusual)")

# Check 4: Deformation always leads to PIT_NOW?
deformation_strategies = df[df['sidewall_deformation'] == True]['strategy'].value_counts()
print(f"✓ Strategies when deformation detected:")
print(deformation_strategies)
if 'PIT_NOW' not in deformation_strategies.index or len(deformation_strategies) > 1:
    print("  ⚠ Warning: Deformation should ALWAYS trigger PIT_NOW")

print()
print("="*60)
print("EDGE CASES PREVIEW")
print("="*60)
print(edge_df[['compound', 'lap_number', 'strategy', 'scenario_name']])
print()

print("="*60)
print("✓ DATA INSPECTION COMPLETE!")
print("="*60)
print()
print("Next step: Train the model!")
print("Run: python src/train_model.py")