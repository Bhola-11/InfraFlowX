from django.test import TestCase
from apps.conditions.sensor_fusion import KalmanSensorFusionEngine


class ConditionsEngineeringTestCase(TestCase):
    def test_kalman_filter(self):
        kf = KalmanSensorFusionEngine(initial_state=100.0)
        measurements = [98.0, 97.5, 96.0, 95.2, 94.0]
        results = kf.process_sensor_stream(measurements)
        self.assertEqual(len(results), 5)
        self.assertLess(results[-1]["kalman_estimated_condition"], 100.0)
