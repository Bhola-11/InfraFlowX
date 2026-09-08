from django.test import TestCase
from apps.assets.risk_matrix import AssetRiskMatrixEngine


class AssetsEngineeringTestCase(TestCase):
    def test_business_risk_exposure(self):
        res = AssetRiskMatrixEngine.calculate_business_risk_exposure(
            condition_score=65.0,
            age_years=15.0,
            expected_life_years=25.0,
            safety_impact=4,
            environmental_impact=3,
        )
        self.assertIn("business_risk_exposure_score", res)
        self.assertTrue(0 <= res["business_risk_exposure_score"] <= 25.0)
