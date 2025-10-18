import pandas as pd
import numpy as np
from datetime import datetime
import random

class F1TireDataGenerator:
    """
    Generates synthetic F1 tire data based on real racing logic and physics
    """
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        
        # Compound definitions based on Pirelli F1 tires
        self.compounds = {
            'soft': {
                'color': 'red',
                'expected_life': 22,  # laps
                'optimal_temp_range': (95, 105),
                'degradation_rate': 1.8,
                'pressure_range': (19.5, 21.0),
                'graining_susceptibility': 0.7
            },
            'medium': {
                'color': 'yellow',
                'expected_life': 32,
                'optimal_temp_range': (100, 110),
                'degradation_rate': 1.2,
                'pressure_range': (19.0, 21.5),
                'graining_susceptibility': 0.4
            },
            'hard': {
                'color': 'white',
                'expected_life': 45,
                'optimal_temp_range': (105, 115),
                'degradation_rate': 0.8,
                'pressure_range': (18.5, 21.0),
                'graining_susceptibility': 0.3
            },
            'intermediate': {
                'color': 'green',
                'expected_life': 15,
                'optimal_temp_range': (85, 95),
                'degradation_rate': 2.0,
                'pressure_range': (18.0, 20.0),
                'graining_susceptibility': 0.5
            },
            'wet': {
                'color': 'blue',
                'expected_life': 10,
                'optimal_temp_range': (75, 85),
                'degradation_rate': 2.5,
                'pressure_range': (17.5, 19.5),
                'graining_susceptibility': 0.3
            }
        }
        
        self.wear_patterns = ['even', 'inner', 'outer', 'center', 'uneven']
        
    def generate_dataset(self, n_samples=10000):
        """
        Generate complete synthetic dataset
        """
        data = []
        
        # Distribution weights for realistic scenarios
        # 60% normal racing, 15% aggressive, 10% weather transitions, 
        # 10% incidents, 5% strategy gambles
        scenario_types = ['normal', 'aggressive', 'weather', 'incident', 'strategy']
        scenario_weights = [0.60, 0.15, 0.10, 0.10, 0.05]
        
        for i in range(n_samples):
            scenario = random.choices(scenario_types, weights=scenario_weights)[0]
            sample = self._generate_sample(scenario)
            data.append(sample)
        
        df = pd.DataFrame(data)
        
        # Add derived features
        df = self._add_derived_features(df)
        
        return df
    
    def _generate_sample(self, scenario_type):
        """
        Generate a single tire data sample
        """
        # Select compound (weighted by typical F1 usage)
        compound_weights = [0.35, 0.40, 0.20, 0.03, 0.02]  # soft, med, hard, inter, wet
        compound = random.choices(list(self.compounds.keys()), weights=compound_weights)[0]
        
        compound_info = self.compounds[compound]
        expected_life = compound_info['expected_life']
        
        # Generate lap number based on scenario
        if scenario_type == 'normal':
            lap_number = int(np.random.uniform(1, expected_life * 0.95))
        elif scenario_type == 'aggressive':
            lap_number = int(np.random.uniform(1, expected_life * 0.85))
        elif scenario_type == 'weather':
            lap_number = int(np.random.uniform(1, expected_life * 0.60))
        elif scenario_type == 'incident':
            lap_number = int(np.random.uniform(expected_life * 0.3, expected_life * 0.70))
        else:  # strategy gamble
            lap_number = int(np.random.uniform(expected_life * 0.85, expected_life * 1.15))
        
        lap_number = max(1, lap_number)
        
        # Calculate wear percentage
        wear_percentage = lap_number / expected_life
        
        # Generate track temperature (depends on scenario)
        if compound in ['intermediate', 'wet']:
            track_temp = int(np.random.uniform(10, 25))
        else:
            if scenario_type == 'weather':
                track_temp = int(np.random.uniform(15, 30))
            else:
                track_temp = int(np.random.uniform(20, 45))
        
        # Generate tire temperature (correlated with track temp and compound)
        optimal_temp_min, optimal_temp_max = compound_info['optimal_temp_range']
        
        if wear_percentage < 0.2:  # Early stint - warming up
            temp_offset = np.random.uniform(-10, 0)
        elif wear_percentage < 0.7:  # Peak performance
            temp_offset = np.random.uniform(-5, 5)
        else:  # Late stint - overheating
            temp_offset = np.random.uniform(0, 15)
        
        tyre_temp = int(track_temp + np.random.uniform(5, 15) + temp_offset)
        
        # Generate tire pressure (affected by temperature and wear)
        base_pressure = np.random.uniform(*compound_info['pressure_range'])
        pressure_variance = np.random.uniform(-1.5, 1.5)
        
        # Pressure drops with wear or rises with overheating
        if wear_percentage > 0.8 or tyre_temp > optimal_temp_max + 10:
            pressure_variance += np.random.uniform(-1, 0.5)
        
        tyre_pressure = round(base_pressure + pressure_variance, 1)
        
        # Generate wear pattern based on scenario and wear
        if scenario_type == 'aggressive' or wear_percentage > 0.75:
            wear_pattern = random.choices(
                self.wear_patterns, 
                weights=[0.2, 0.25, 0.25, 0.15, 0.15]
            )[0]
        elif scenario_type == 'incident':
            wear_pattern = random.choices(
                self.wear_patterns, 
                weights=[0.1, 0.2, 0.2, 0.1, 0.4]
            )[0]
        else:
            wear_pattern = random.choices(
                self.wear_patterns, 
                weights=[0.6, 0.15, 0.15, 0.05, 0.05]
            )[0]
        
        # Generate graining (more likely early stint, cold temps, soft compounds)
        graining_prob = compound_info['graining_susceptibility']
        if lap_number < 8 and track_temp < 25:
            graining_prob *= 2.5
        if tyre_temp < optimal_temp_min:
            graining_prob *= 1.5
        
        is_graining = random.random() < min(graining_prob, 0.95)
        
        # Generate sidewall deformation (critical failure - rare)
        deformation_prob = 0.01
        if wear_percentage > 1.0:
            deformation_prob = 0.25
        elif wear_percentage > 0.9:
            deformation_prob = 0.08
        elif tyre_pressure < 17 or tyre_pressure > 24:
            deformation_prob = 0.15
        
        sidewall_deformation = random.random() < deformation_prob
        
        # Determine strategy based on all factors
        strategy = self._determine_strategy(
            compound, lap_number, expected_life, wear_pattern,
            sidewall_deformation, tyre_pressure, is_graining,
            tyre_temp, track_temp, optimal_temp_min, optimal_temp_max
        )
        
        return {
            'color': compound_info['color'],
            'compound': compound,
            'lap_number': lap_number,
            'wear_pattern': wear_pattern,
            'sidewall_deformation': sidewall_deformation,
            'tyre_pressure': tyre_pressure,
            'is_graining': is_graining,
            'tyre_temperature': tyre_temp,
            'track_temperature': track_temp,
            'strategy': strategy
        }
    
    def _determine_strategy(self, compound, lap_num, expected_life, wear_pattern,
                           deformation, pressure, graining, tyre_temp, track_temp,
                           opt_temp_min, opt_temp_max):
        """
        Determine racing strategy based on tire conditions
        """
        wear_percentage = lap_num / expected_life
        
        # CRITICAL: Immediate pit conditions
        if deformation:
            return 'PIT_NOW'
        
        if pressure < 17 or pressure > 24:
            return 'PIT_NOW'
        
        if wear_percentage >= 1.0:
            return 'PIT_NOW'
        
        if wear_pattern == 'uneven' and wear_percentage > 0.80:
            return 'PIT_NOW'
        
        # PIT SOON conditions
        if wear_percentage >= 0.85:
            return 'PIT_SOON'
        
        if tyre_temp > opt_temp_max + 15:
            return 'PIT_SOON'
        
        if graining and compound == 'soft' and lap_num > 15:
            return 'PIT_SOON'
        
        if wear_pattern in ['center', 'inner', 'outer'] and wear_percentage > 0.75:
            return 'PIT_SOON'
        
        # PUSH conditions (good tire state)
        if (wear_percentage < 0.60 and 
            wear_pattern == 'even' and 
            opt_temp_min <= tyre_temp <= opt_temp_max and
            not graining and
            19 <= pressure <= 21.5):
            return 'PUSH'
        
        # CONSERVE conditions (managing degradation)
        if wear_percentage > 0.70 and wear_percentage < 0.85:
            return 'CONSERVE'
        
        if track_temp > 40:
            return 'CONSERVE'
        
        if graining and lap_num < 12:
            return 'CONSERVE'
        
        # Default: MONITOR
        return 'MONITOR'
    
    def _add_derived_features(self, df):
        """
        Add calculated features for better model performance
        """
        # Map compound to expected life for calculations
        compound_life_map = {k: v['expected_life'] for k, v in self.compounds.items()}
        df['expected_life'] = df['compound'].map(compound_life_map)
        
        # Lap percentage
        df['lap_percentage'] = df['lap_number'] / df['expected_life']
        
        # Temperature differential
        df['temp_differential'] = df['tyre_temperature'] - df['track_temperature']
        
        # Pressure optimal flag
        df['is_pressure_optimal'] = df['tyre_pressure'].between(19, 21.5)
        
        # Temperature optimal flag (simplified)
        df['is_temp_optimal'] = df['tyre_temperature'].between(95, 115)
        
        # Wear severity score
        wear_severity_map = {
            'even': 0,
            'inner': 2,
            'outer': 2,
            'center': 3,
            'uneven': 4
        }
        df['wear_severity'] = df['wear_pattern'].map(wear_severity_map)
        
        # Risk score (composite metric)
        df['risk_score'] = (
            df['lap_percentage'] * 40 +
            df['wear_severity'] * 10 +
            df['sidewall_deformation'].astype(int) * 50 +
            df['is_graining'].astype(int) * 15 +
            (~df['is_pressure_optimal']).astype(int) * 10 +
            (~df['is_temp_optimal']).astype(int) * 5
        )
        
        return df
    
    def generate_edge_cases(self):
        """
        Generate specific edge case scenarios for testing
        """
        edge_cases = [
            # Monaco rain scenario
            {
                'color': 'green',
                'compound': 'intermediate',
                'lap_number': 3,
                'wear_pattern': 'even',
                'sidewall_deformation': False,
                'tyre_pressure': 19.5,
                'is_graining': False,
                'tyre_temperature': 88,
                'track_temperature': 18,
                'strategy': 'MONITOR',
                'scenario_name': 'Monaco_rain_start'
            },
            # Silverstone blowout risk
            {
                'color': 'white',
                'compound': 'hard',
                'lap_number': 42,
                'wear_pattern': 'outer',
                'sidewall_deformation': False,
                'tyre_pressure': 16.5,
                'is_graining': False,
                'tyre_temperature': 118,
                'track_temperature': 35,
                'strategy': 'PIT_NOW',
                'scenario_name': 'Silverstone_blowout_risk'
            },
            # Singapore overheating
            {
                'color': 'yellow',
                'compound': 'medium',
                'lap_number': 28,
                'wear_pattern': 'center',
                'sidewall_deformation': False,
                'tyre_pressure': 22.5,
                'is_graining': False,
                'tyre_temperature': 125,
                'track_temperature': 45,
                'strategy': 'PIT_SOON',
                'scenario_name': 'Singapore_overheating'
            },
            # Barcelona cold graining
            {
                'color': 'red',
                'compound': 'soft',
                'lap_number': 6,
                'wear_pattern': 'uneven',
                'sidewall_deformation': False,
                'tyre_pressure': 20.0,
                'is_graining': True,
                'tyre_temperature': 88,
                'track_temperature': 16,
                'strategy': 'CONSERVE',
                'scenario_name': 'Barcelona_cold_graining'
            },
            # Perfect push conditions
            {
                'color': 'red',
                'compound': 'soft',
                'lap_number': 8,
                'wear_pattern': 'even',
                'sidewall_deformation': False,
                'tyre_pressure': 20.5,
                'is_graining': False,
                'tyre_temperature': 102,
                'track_temperature': 28,
                'strategy': 'PUSH',
                'scenario_name': 'Perfect_push_conditions'
            },
            # Critical deformation
            {
                'color': 'yellow',
                'compound': 'medium',
                'lap_number': 25,
                'wear_pattern': 'even',
                'sidewall_deformation': True,
                'tyre_pressure': 20.0,
                'is_graining': False,
                'tyre_temperature': 105,
                'track_temperature': 30,
                'strategy': 'PIT_NOW',
                'scenario_name': 'Critical_sidewall_deformation'
            },
        ]
        
        df = pd.DataFrame(edge_cases)
        return df
    
    def save_datasets(self, output_dir='data/generated'):
        """
        Generate and save all datasets
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate main dataset
        print("Generating main dataset...")
        main_df = self.generate_dataset(n_samples=10000)
        main_df.to_csv(f'{output_dir}/f1_tire_data.csv', index=False)
        print(f"✓ Saved main dataset: {len(main_df)} samples")
        
        # Generate edge cases
        print("Generating edge cases...")
        edge_df = self.generate_edge_cases()
        edge_df.to_csv(f'{output_dir}/edge_cases.csv', index=False)
        print(f"✓ Saved edge cases: {len(edge_df)} samples")
        
        # Print statistics
        print("\n=== Dataset Statistics ===")
        print("\nStrategy Distribution:")
        print(main_df['strategy'].value_counts(normalize=True).mul(100).round(1))
        print("\nCompound Distribution:")
        print(main_df['compound'].value_counts(normalize=True).mul(100).round(1))
        print("\nWear Pattern Distribution:")
        print(main_df['wear_pattern'].value_counts(normalize=True).mul(100).round(1))
        
        return main_df, edge_df


# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("F1 TIRE STRATEGY - DATA GENERATION")
    print("=" * 60)
    print()
    
    generator = F1TireDataGenerator(seed=42)
    main_df, edge_df = generator.save_datasets()
    
    print("\n✓ Data generation complete!")
    print("\nNext steps:")
    print("1. Run exploratory data analysis (EDA)")
    print("2. Build and train your model")
    print("3. Test on edge cases")