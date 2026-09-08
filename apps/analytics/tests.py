from django.test import TestCase
from apps.analytics.anomaly_detector import SensorAnomalyDetectorEngine
from apps.analytics.spatial_statistics import SpatialStatisticsEngine
from apps.analytics.executive_kpi import ExecutiveKPIEngine


class AnalyticsEngineeringTestCase(TestCase):
    def test_anomaly_detection(self):
        series = [10.0, 10.2, 9.8, 10.1, 55.0, 10.0, 9.9]
        res = SensorAnomalyDetectorEngine.detect_zscore_anomalies(series, threshold_z=2.0)
        self.assertGreater(res["anomaly_count"], 0)

    def test_spatial_statistics(self):
        coords = [(37.77, -122.41), (37.78, -122.42)]
        centroid = SpatialStatisticsEngine.compute_spatial_centroid(coords)
        self.assertAlmostEqual(centroid[0], 37.775, places=3)

    def test_executive_kpi(self):
        res = ExecutiveKPIEngine.calculate_infrastructure_health_index(
            avg_asset_condition_pct=88.0,
            pm_compliance_pct=92.0,
            capital_backlog_ratio_fci=0.04,
            critical_incident_rate_per_100=0.5
        )
        self.assertIn(res["operational_tier"], ["OPTIMAL", "SATISFACTORY"])
