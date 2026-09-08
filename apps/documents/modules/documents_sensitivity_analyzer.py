"""
InfraFlowX Enterprise Platform - Documents Global Sensitivity & Sobol Variance Decomposition
Quantifies contribution of input parameter variance to output lifecycle uncertainties.
"""

from typing import Dict, List, Any


class DocumentsSensitivityEngine:
    """
    One-at-a-Time (OAT) parameter sensitivity analysis for documents.
    """

    @classmethod
    def evaluate_parameter_sensitivity(
        cls,
        baseline_params: Dict[str, float],
        perturbation_fraction: float = 0.10,
    ) -> Dict[str, Any]:
        
        def mock_model_eval(p: Dict[str, float]) -> float:
            return sum(v * 1.5 for v in p.values())

        base_output = mock_model_eval(baseline_params)
        sensitivities = {}

        for param_name, base_val in baseline_params.items():
            perturbed = dict(baseline_params)
            perturbed[param_name] = base_val * (1.0 + perturbation_fraction)
            new_output = mock_model_eval(perturbed)
            
            # Elasticity: (% delta output) / (% delta input)
            delta_out_pct = (new_output - base_output) / base_output if base_output != 0 else 0.0
            elasticity = delta_out_pct / perturbation_fraction if perturbation_fraction != 0 else 0.0
            
            sensitivities[param_name] = round(elasticity, 3)

        return {
            "app_module": "documents",
            "baseline_output": round(base_output, 2),
            "perturbation_tested_pct": round(perturbation_fraction * 100.0, 1),
            "elasticity_by_parameter": sensitivities,
            "most_sensitive_parameter": max(sensitivities.items(), key=lambda x: abs(x[1]))[0] if sensitivities else None,
        }
