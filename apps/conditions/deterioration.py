"""
Markovian Asset Deterioration & Predictive Decay Engine
Simulates state-to-state transition probability matrices for infrastructure degradation.
"""
from decimal import Decimal
import numpy as np


class MarkovDeteriorationEngine:
    """
    Simulates condition decay across 5 states:
    State 1: Excellent (90-100)
    State 2: Good (70-89)
    State 3: Fair (50-69)
    State 4: Poor (25-49)
    State 5: Critical (0-24)
    """
    BASELINE_MATRICES = {
        'ROAD': np.array([
            [0.85, 0.13, 0.02, 0.00, 0.00],
            [0.00, 0.80, 0.16, 0.04, 0.00],
            [0.00, 0.00, 0.75, 0.20, 0.05],
            [0.00, 0.00, 0.00, 0.70, 0.30],
            [0.00, 0.00, 0.00, 0.00, 1.00],
        ]),
        'BRIDGE': np.array([
            [0.94, 0.05, 0.01, 0.00, 0.00],
            [0.00, 0.90, 0.08, 0.02, 0.00],
            [0.00, 0.00, 0.85, 0.12, 0.03],
            [0.00, 0.00, 0.00, 0.80, 0.20],
            [0.00, 0.00, 0.00, 0.00, 1.00],
        ]),
        'BUILDING': np.array([
            [0.92, 0.07, 0.01, 0.00, 0.00],
            [0.00, 0.88, 0.10, 0.02, 0.00],
            [0.00, 0.00, 0.82, 0.15, 0.03],
            [0.00, 0.00, 0.00, 0.78, 0.22],
            [0.00, 0.00, 0.00, 0.00, 1.00],
        ]),
        'FACILITY': np.array([
            [0.88, 0.10, 0.02, 0.00, 0.00],
            [0.00, 0.84, 0.13, 0.03, 0.00],
            [0.00, 0.00, 0.78, 0.18, 0.04],
            [0.00, 0.00, 0.00, 0.72, 0.28],
            [0.00, 0.00, 0.00, 0.00, 1.00],
        ]),
    }

    @classmethod
    def forecast_decay_profile(cls, asset_type, initial_state_idx=0, years=10, load_multiplier=1.0, climate_multiplier=1.0):
        matrix = cls.BASELINE_MATRICES.get(asset_type, cls.BASELINE_MATRICES['ROAD']).copy()
        
        # Apply environmental & traffic load factors
        penalty = float(load_multiplier) * float(climate_multiplier)
        if penalty > 1.0:
            for i in range(4):
                diag = matrix[i, i]
                decay = 1.0 - diag
                accelerated_decay = min(0.40, decay * penalty)
                matrix[i, i] = 1.0 - accelerated_decay
                matrix[i, i + 1] = accelerated_decay

        state_vector = np.zeros(5)
        state_vector[initial_state_idx] = 1.0

        yearly_states = []
        score_weights = np.array([95.0, 80.0, 60.0, 37.0, 12.0])

        current_v = state_vector
        for yr in range(1, years + 1):
            current_v = np.dot(current_v, matrix)
            expected_score = float(np.dot(current_v, score_weights))
            yearly_states.append({
                'year': yr,
                'state_probabilities': [round(float(p), 4) for p in current_v],
                'expected_condition_score': round(expected_score, 1),
                'dominant_state': int(np.argmax(current_v)) + 1
            })

        return yearly_states
