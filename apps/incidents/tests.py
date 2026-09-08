from django.test import TestCase
from apps.incidents.root_cause_analysis import RootCauseAnalysisEngine
from apps.incidents.emergency_response_flow import EmergencyResponseWorkflowEngine
from apps.incidents.osha_reporting import OSHAReportingEngine


class IncidentsEngineeringTestCase(TestCase):
    def test_root_cause_analysis(self):
        whys = ["Pump stopped", "Bearing overheated", "Lubrication leak", "Seal degraded", "Preventive schedule missed"]
        factors = [{"category": "MACHINE_EQUIPMENT", "factor": "Bearing wear"}]
        res = RootCauseAnalysisEngine.compile_rca_report("INC-001", "Pump Failure", whys, factors)
        self.assertEqual(res["root_cause_determination"], "Preventive schedule missed")

    def test_emergency_severity(self):
        res = EmergencyResponseWorkflowEngine.assess_incident_severity(
            casualties_count=0,
            affected_population=5000,
            critical_infrastructure_impassable=True,
            hazardous_materials_spill=False
        )
        self.assertIn("recommended_ics_activation_level", res)

    def test_dart_rate(self):
        res = OSHAReportingEngine.calculate_dart_rate(days_away_cases=1, job_transfer_cases=0, total_hours_worked=200000.0)
        self.assertAlmostEqual(res["dart_rate"], 1.0, places=1)
