from django.test import TestCase
from apps.inspections.checklist_engine import InspectionChecklistEngine, InspectionItemResponse
from apps.inspections.drone_telemetry import DronePhotogrammetryEngine
from apps.inspections.nondestructive_testing import NonDestructiveTestingEngine


class InspectionsEngineeringTestCase(TestCase):
    def test_checklist_scoring(self):
        items = [
            InspectionItemResponse(item_id="1", category="DECK", score=4, weight=1.0),
            InspectionItemResponse(item_id="2", category="SUBSTRUCTURE", score=5, weight=1.5),
        ]
        res = InspectionChecklistEngine.score_inspection(items)
        self.assertIn("overall_score_percentage", res)
        self.assertGreater(res["overall_score_percentage"], 70.0)

    def test_drone_gsd(self):
        res = DronePhotogrammetryEngine.calculate_ground_sampling_distance(
            flight_altitude_m=30.0,
            focal_length_mm=24.0,
            sensor_width_mm=13.2,
            image_width_pixels=4000,
        )
        self.assertIn("ground_sampling_distance_cm_per_pixel", res)

    def test_ndt_ultrasonic(self):
        res = NonDestructiveTestingEngine.evaluate_ultrasonic_pulse_velocity(path_length_mm=200.0, transit_time_microseconds=50.0)
        self.assertEqual(res["concrete_quality_grade"], "GOOD")
