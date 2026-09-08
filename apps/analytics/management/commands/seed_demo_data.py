import random
import uuid
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.organizations.models import Organization, Region, Zone, Department, Office, Team
from apps.employees.models import Designation, Skill, Certification, Employee
from apps.locations.models import Location
from apps.assets.models import AssetCategory, Asset, AssetStatusHistory
from apps.roads.models import Road, RoadDefect, RoadRepairHistory
from apps.bridges.models import Bridge, BridgeComponentInspection
from apps.buildings.models import Building, BuildingFloor
from apps.facilities.models import FacilityEquipment, FacilityServiceLog
from apps.inspections.models import Inspection, InspectionChecklistItem
from apps.conditions.models import ConditionLog, DeteriorationModel
from apps.maintenance.models import MaintenancePlan, MaintenanceActionLog
from apps.workorders.models import WorkOrder, WorkOrderTask
from apps.projects.models import Project, ProjectMilestone
from apps.contractors.models import Contractor, ContractAgreement, ContractorEvaluation
from apps.budgets.models import Budget, BudgetAllocation
from apps.expenses.models import Expense
from apps.incidents.models import Incident, IncidentDispatchLog
from apps.documents.models import DocumentCategory, Document, BlueprintMetadata
from apps.inventory.models import Warehouse, InventoryCategory, SparePart, StockItem, StockMovementLedger, PurchaseRequisition, PurchaseRequisitionItem
from apps.schedules.models import AssetSchedule, ScheduledEventExecution
from apps.support.models import SLAPolicy, SupportTicket, TicketComment
from apps.reports.models import ReportTemplate
from apps.analytics.models import KPITarget, InfrastructureHealthIndex
from apps.notifications.utils import send_notification
from apps.audit.utils import log_audit_event

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds realistic enterprise demonstration data for InfraFlowX platform.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting InfraFlowX Enterprise Data Seeder...'))

        # 1. Superuser & Staff Accounts
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@infraflowx.gov',
                'first_name': 'Chief',
                'last_name': 'Administrator',
                'role': 'SUPER_ADMIN',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))

        # Standard role users
        users = [admin_user]
        user_roles = [
            ('engineer1', 'Rajesh', 'Sharma', 'CHIEF_ENGINEER', 'rajesh.sharma@infraflowx.gov'),
            ('inspector1', 'Anita', 'Deshmukh', 'SENIOR_INSPECTOR', 'anita.d@infraflowx.gov'),
            ('planner1', 'Vikram', 'Mehta', 'MAINTENANCE_PLANNER', 'vikram.m@infraflowx.gov'),
            ('finance1', 'Suresh', 'Nair', 'BUDGET_OFFICER', 'suresh.nair@infraflowx.gov'),
            ('dispatcher1', 'Pooja', 'Verma', 'DISPATCH_COORDINATOR', 'pooja.v@infraflowx.gov'),
        ]
        for uname, fname, lname, role, email in user_roles:
            u, _ = User.objects.get_or_create(
                username=uname,
                defaults={'first_name': fname, 'last_name': lname, 'role': role, 'email': email, 'is_staff': True}
            )
            u.set_password('password123')
            u.save()
            users.append(u)

        # 2. Organizations & Governance Hierarchy
        org, _ = Organization.objects.get_or_create(
            code='NDMC-INFRA',
            defaults={
                'name': 'National Capital Infrastructure & Public Works Authority',
                'org_type': 'MUNICIPAL',
                'tax_id': 'GSTIN07NDMC2026M1Z',
                'email': 'contact@ndmc-infra.gov.in',
                'phone': '+91-11-23348000',
                'website': 'https://infraflowx.gov.in',
                'address': 'Palika Kendra, Sansad Marg, New Delhi 110001',
                'annual_budget': Decimal('1500000000.00'),
            }
        )

        region_north, _ = Region.objects.get_or_create(code='DEL-NORTH', defaults={'organization': org, 'name': 'Northern Capital Region'})
        region_south, _ = Region.objects.get_or_create(code='DEL-SOUTH', defaults={'organization': org, 'name': 'Southern Capital Corridor'})

        zone1, _ = Zone.objects.get_or_create(code='Z-CIVIL-LINES', defaults={'region': region_north, 'name': 'Civil Lines & Ridge Corridor'})
        zone2, _ = Zone.objects.get_or_create(code='Z-CHANAKYA', defaults={'region': region_south, 'name': 'Chanakyapuri Diplomatic Enclave'})

        dept_highways, _ = Department.objects.get_or_create(code='DEPT-HWY', defaults={'organization': org, 'name': 'Highways, Bridges & Pavements Dept'})
        dept_facilities, _ = Department.objects.get_or_create(code='DEPT-FAC', defaults={'organization': org, 'name': 'Public Buildings & MEP Facilities Dept'})
        dept_disaster, _ = Department.objects.get_or_create(code='DEPT-DRM', defaults={'organization': org, 'name': 'Emergency Dispatch & Hazard Response Dept'})

        office1, _ = Office.objects.get_or_create(name='Central Engineering Secretariat', defaults={'organization': org, 'region': region_north, 'office_type': 'DIVISION', 'address': 'Barakhamba Road, New Delhi'})
        team_rapid, _ = Team.objects.get_or_create(code='TEAM-RAPID-01', defaults={'department': dept_highways, 'office': office1, 'name': 'Rapid Pothole & Surface Repair Unit', 'team_lead': users[1], 'specialization': 'Asphalt Paving & Pothole Repair'})
        team_bridge, _ = Team.objects.get_or_create(code='TEAM-BRIDGE-01', defaults={'department': dept_highways, 'office': office1, 'name': 'Bridge & Structural Health Inspection Squad', 'team_lead': users[2], 'specialization': 'Structural NDT & Cable Inspection'})

        # 3. Designations & Employees
        desig_chief, _ = Designation.objects.get_or_create(code='CE-01', defaults={'title': 'Chief Civil Engineer', 'level': 5})
        desig_insp, _ = Designation.objects.get_or_create(code='IN-01', defaults={'title': 'Senior Structural Inspector', 'level': 3})

        emp1, _ = Employee.objects.get_or_create(
            employee_id='EMP-1001',
            defaults={
                'user': users[1],
                'organization': org,
                'department': dept_highways,
                'office': office1,
                'designation': desig_chief,
                'team': team_rapid,
                'status': 'ACTIVE',
                'date_of_joining': '2020-01-15',
                'salary': Decimal('1200000.00'),
            }
        )

        # 4. GIS Locations (Coordinates in Delhi-NCR)
        loc_data = [
            ('LOC-DEL-01', 'Ring Road - AIIMS Flyover Junction', 28.5672, 77.2100, 'Ring Rd, Ansari Nagar, New Delhi', 'Ansari Nagar', 'New Delhi', 'Delhi', '110029'),
            ('LOC-DEL-02', 'Signature Bridge Eastern Pylon Approach', 28.7061, 77.2341, 'Wazirabad, Yamuna Riverfront, Delhi', 'Wazirabad', 'Delhi', 'Delhi', '110054'),
            ('LOC-DEL-03', 'Barapullah Elevated Corridor Phase II', 28.5833, 77.2458, 'JLN Stadium to Sarai Kale Khan, New Delhi', 'Lodi Road', 'New Delhi', 'Delhi', '110003'),
            ('LOC-DEL-04', 'Civic Centre Headquarters Complex', 28.6448, 77.2289, 'Jawaharlal Nehru Marg, Minto Road, New Delhi', 'Minto Road', 'New Delhi', 'Delhi', '110002'),
            ('LOC-DEL-05', 'Indira Gandhi Indoor Stadium & Sports Complex', 28.6292, 77.2478, 'IP Estate, Ring Road, New Delhi', 'IP Estate', 'New Delhi', 'Delhi', '110002'),
            ('LOC-DEL-06', 'DND Flyway Yamuna Bridge', 28.5700, 77.2790, 'Delhi Noida Direct Toll Plaza, New Delhi', 'Maharani Bagh', 'New Delhi', 'Delhi', '110014'),
            ('LOC-DEL-07', 'Outer Ring Road Subroto Park Underpass', 28.5815, 77.1500, 'Subroto Park, Airport Expressway, New Delhi', 'Dhaula Kuan', 'New Delhi', 'Delhi', '110010'),
            ('LOC-DEL-08', 'Vikas Minar DDA Central Tower', 28.6300, 77.2490, 'ITO Crossing, Vikas Marg, New Delhi', 'ITO', 'New Delhi', 'Delhi', '110002'),
        ]
        locations = []
        for code, name, lat, lng, addr, area, city, state, postal in loc_data:
            loc, _ = Location.objects.get_or_create(
                code=code,
                defaults={
                    'organization': org,
                    'name': name,
                    'latitude': Decimal(str(lat)),
                    'longitude': Decimal(str(lng)),
                    'address': addr,
                    'area': area,
                    'city': city,
                    'state': state,
                    'postal_code': postal,
                    'country': 'India',
                }
            )
            locations.append(loc)

        # 5. Asset Categories & Infrastructure Assets
        cat_roads, _ = AssetCategory.objects.get_or_create(code='CAT-ROAD', defaults={'name': 'Highways, Expressways & Urban Corridors'})
        cat_bridges, _ = AssetCategory.objects.get_or_create(code='CAT-BRIDGE', defaults={'name': 'Cable-Stayed, Flyover & River Bridges'})
        cat_buildings, _ = AssetCategory.objects.get_or_create(code='CAT-BLDG', defaults={'name': 'Municipal Towers, Administrative Complexes'})
        cat_facilities, _ = AssetCategory.objects.get_or_create(code='CAT-FAC', defaults={'name': 'Pumping Stations, Stadiums & Water Treatment'})

        # Assets Creation
        assets = []
        
        # Asset 1: Ring Road Arterial
        a1, _ = Asset.objects.get_or_create(
            asset_id='AST-ROAD-001',
            defaults={
                'name': 'Mahatma Gandhi Inner Ring Road (AIIMS to Moti Bagh Section)',
                'asset_type': 'ROAD',
                'category': cat_roads,
                'organization': org,
                'department': dept_highways,
                'location': locations[0],
                'status': 'ACTIVE',
                'condition': 'GOOD',
                'condition_score': 88,
                'acquisition_cost': Decimal('145000000.00'),
                'current_value': Decimal('132000000.00'),
                'installation_date': '2016-04-12',
                'useful_life_years': 30,
                'description': 'Dual 4-lane high density arterial corridor carrying 120,000 PCU/day with storm drainage utilities.'
            }
        )
        Road.objects.get_or_create(
            asset=a1,
            defaults={
                'road_code': 'NH-48-RING',
                'road_name': 'Inner Ring Road Arterial',
                'surface_type': 'ASPHALT',
                'length_km': Decimal('8.45'),
                'width_meters': Decimal('24.00'),
                'lanes_count': 8,
                'speed_limit_mph': 45,
                'traffic_level': 'VERY_HIGH',
                'pci_score': 84,
            }
        )
        assets.append(a1)

        # Asset 2: Signature Cable Bridge
        a2, _ = Asset.objects.get_or_create(
            asset_id='AST-BRG-002',
            defaults={
                'name': 'Yamuna Signature Cable-Stayed Bridge & Approaches',
                'asset_type': 'BRIDGE',
                'category': cat_bridges,
                'organization': org,
                'department': dept_highways,
                'location': locations[1],
                'status': 'ACTIVE',
                'condition': 'EXCELLENT',
                'condition_score': 94,
                'acquisition_cost': Decimal('1518000000.00'),
                'current_value': Decimal('1480000000.00'),
                'installation_date': '2018-11-04',
                'useful_life_years': 100,
                'description': 'Iconic 154m high asymmetrical steel pylon cable-stayed bridge spanning Yamuna river with 8-lane carriageway.'
            }
        )
        Bridge.objects.get_or_create(
            asset=a2,
            defaults={
                'bridge_id_code': 'BRG-YAM-01',
                'bridge_name': 'Signature Bridge Yamuna',
                'feature_crossed': 'Yamuna River & Floodplain',
                'bridge_type': 'CABLE_STAYED',
                'length_meters': Decimal('675.00'),
                'width_meters': Decimal('35.20'),
                'span_count': 4,
                'main_span_length': Decimal('251.00'),
                'construction_year': 2018,
                'load_capacity_tons': Decimal('120.00'),
                'condition': 'EXCELLENT',
            }
        )
        assets.append(a2)

        # Asset 3: Barapullah Elevated Flyover
        a3, _ = Asset.objects.get_or_create(
            asset_id='AST-BRG-003',
            defaults={
                'name': 'Barapullah Elevated Expressway Flyover Viaduct',
                'asset_type': 'BRIDGE',
                'category': cat_bridges,
                'organization': org,
                'department': dept_highways,
                'location': locations[2],
                'status': 'ACTIVE',
                'condition': 'GOOD',
                'condition_score': 81,
                'acquisition_cost': Decimal('530000000.00'),
                'current_value': Decimal('490000000.00'),
                'installation_date': '2015-08-20',
                'useful_life_years': 60,
                'description': 'Prestressed concrete box girder viaduct connecting South Delhi to Sarai Kale Khan transit hub.'
            }
        )
        Bridge.objects.get_or_create(
            asset=a3,
            defaults={
                'bridge_id_code': 'BRG-BARA-02',
                'bridge_name': 'Barapullah Phase II Viaduct',
                'feature_crossed': 'Barapullah Nallah & Northern Railway Tracks',
                'bridge_type': 'PRESTRESSED_GIRDER',
                'length_meters': Decimal('3850.00'),
                'width_meters': Decimal('17.50'),
                'span_count': 110,
                'main_span_length': Decimal('35.00'),
                'construction_year': 2015,
                'load_capacity_tons': Decimal('70.00'),
                'condition': 'GOOD',
            }
        )
        assets.append(a3)

        # Asset 4: Civic Centre Tower Complex
        a4, _ = Asset.objects.get_or_create(
            asset_id='AST-BLD-004',
            defaults={
                'name': 'Dr. S.P. Mukherjee Civic Centre Municipal Secretariat Tower',
                'asset_type': 'BUILDING',
                'category': cat_buildings,
                'organization': org,
                'department': dept_facilities,
                'location': locations[3],
                'status': 'ACTIVE',
                'condition': 'EXCELLENT',
                'condition_score': 91,
                'acquisition_cost': Decimal('650000000.00'),
                'current_value': Decimal('720000000.00'),
                'installation_date': '2010-04-22',
                'useful_life_years': 80,
                'description': '28-storey LEED Gold certified civic skyscraper housing municipal governance chambers and IT command rooms.'
            }
        )
        bldg4, _ = Building.objects.get_or_create(
            asset=a4,
            defaults={
                'building_id_code': 'BLD-CIVIC-01',
                'building_name': 'Civic Centre Tower A',
                'building_type': 'GOVERNMENT',
                'address': 'Jawaharlal Nehru Marg, Minto Road, New Delhi 110002',
                'floor_count': 28,
                'total_area_sqft': Decimal('1250000.00'),
                'construction_year': 2010,
                'occupancy_capacity': 5000,
                'energy_rating': 'LEED_GOLD',
            }
        )
        BuildingFloor.objects.get_or_create(building=bldg4, floor_number=1, defaults={'floor_name': 'Ground Concourse & Public Grievance Hall', 'area_sqft': Decimal('25000.00'), 'usage_type': 'Public Atrium'})
        BuildingFloor.objects.get_or_create(building=bldg4, floor_number=12, defaults={'floor_name': 'Central Engineering & GIS War Room', 'area_sqft': Decimal('18500.00'), 'usage_type': 'Operations Center'})
        assets.append(a4)

        # Asset 5: Indira Gandhi Indoor Stadium Complex
        a5, _ = Asset.objects.get_or_create(
            asset_id='AST-FAC-005',
            defaults={
                'name': 'Indira Gandhi Arena HVAC & Electromechanical Plant',
                'asset_type': 'FACILITY',
                'category': cat_facilities,
                'organization': org,
                'department': dept_facilities,
                'location': locations[4],
                'status': 'UNDER_MAINTENANCE',
                'condition': 'FAIR',
                'condition_score': 74,
                'acquisition_cost': Decimal('320000000.00'),
                'current_value': Decimal('275000000.00'),
                'installation_date': '2010-09-15',
                'useful_life_years': 40,
                'description': '25,000 capacity indoor arena central chiller, MEP substations, and automated fire suppression plant.'
            }
        )
        FacilityEquipment.objects.get_or_create(
            asset=a5,
            equipment_code='EQP-CHILL-01',
            defaults={
                'equipment_name': 'Carrier 1200TR Centrifugal Water Chiller Unit A',
                'equipment_type': 'HVAC_CHILLER',
                'manufacturer': 'Carrier Global Corp',
                'model_number': '19XR-1200',
                'power_rating_kw': Decimal('750.00'),
            }
        )
        assets.append(a5)

        # Additional sample assets to populate diverse dataset
        for i in range(6, 30):
            ast_type = random.choice(['ROAD', 'BRIDGE', 'BUILDING', 'FACILITY'])
            cat = cat_roads if ast_type == 'ROAD' else (cat_bridges if ast_type == 'BRIDGE' else (cat_buildings if ast_type == 'BUILDING' else cat_facilities))
            loc = random.choice(locations)
            c_score = random.randint(52, 98)
            status = 'ACTIVE' if c_score > 70 else ('UNDER_MAINTENANCE' if c_score > 55 else 'DAMAGED')
            cond = 'EXCELLENT' if c_score > 89 else ('GOOD' if c_score > 69 else ('FAIR' if c_score > 49 else 'POOR'))
            
            ast, _ = Asset.objects.get_or_create(
                asset_id=f'AST-GEN-{i:03d}',
                defaults={
                    'name': f'Municipal Infrastructure Section {i} - {loc.name}',
                    'asset_type': ast_type,
                    'category': cat,
                    'organization': org,
                    'department': dept_highways if ast_type in ['ROAD', 'BRIDGE'] else dept_facilities,
                    'location': loc,
                    'status': status,
                    'condition': cond,
                    'condition_score': c_score,
                    'acquisition_cost': Decimal(str(random.randint(15, 120) * 1000000)),
                    'current_value': Decimal(str(random.randint(10, 100) * 1000000)),
                    'installation_date': timezone.now().date() - timedelta(days=random.randint(300, 3650)),
                    'useful_life_years': random.randint(25, 60),
                    'description': f'Public civil asset {i} serving municipal district under {loc.city} administrative zone.'
                }
            )
            assets.append(ast)

        self.stdout.write(self.style.SUCCESS(f'Populated {len(assets)} Infrastructure Assets.'))

        # 6. Contractors & Empanelled Vendors
        contractor1, _ = Contractor.objects.get_or_create(
            registration_number='CON-LNT-01',
            defaults={
                'company_name': 'Larsen & Toubro Heavy Civil Infrastructure Ltd',
                'organization': org,
                'specialization': 'BRIDGE_STRUCTURAL',
                'status': 'ACTIVE',
                'contact_person': 'Arun V. Nambiar',
                'phone': '+91-22-67525656',
                'email': 'civil.tenders@larsentoubro.com',
                'address': 'L&T House, Ballard Estate, Mumbai 400001',
                'rating': Decimal('4.80'),
                'contract_start': '2021-01-01',
                'contract_end': '2028-12-31',
            }
        )
        contractor2, _ = Contractor.objects.get_or_create(
            registration_number='CON-NCC-02',
            defaults={
                'company_name': 'NCC Urban Pavement & Asphalt Infra Ltd',
                'organization': org,
                'specialization': 'ASPHALT_PAVING',
                'status': 'ACTIVE',
                'contact_person': 'M. Somaraju',
                'phone': '+91-40-23351752',
                'email': 'contracts@ncclimited.com',
                'address': 'NCC House, Madhapur, Hyderabad 500081',
                'rating': Decimal('4.50'),
                'contract_start': '2022-04-01',
                'contract_end': '2027-03-31',
            }
        )

        ContractAgreement.objects.get_or_create(
            contract_number='AGR-2026-YAMUNA-01',
            defaults={
                'contract_title': 'Signature Bridge Pier Cable Tensioning & Seismic Damper Retrofit Agreement',
                'contractor': contractor1,
                'organization': org,
                'total_contract_value': Decimal('48500000.00'),
                'start_date': '2026-01-01',
                'end_date': '2027-12-31',
                'scope_summary': 'Pier cable tensioning and seismic retrofit.',
                'is_active': True,
            }
        )
        ContractorEvaluation.objects.get_or_create(
            contractor=contractor1,
            defaults={
                'evaluated_by': users[1],
                'overall_score': Decimal('4.85'),
                'quality_score': 5,
                'timeliness_score': 4,
                'safety_score': 5,
                'comments': 'Exceptional precision in structural steel tension testing and laser deflection measurement.'
            }
        )

        # 7. Capital Projects & Milestones
        proj1, _ = Project.objects.get_or_create(
            project_id='PRJ-2026-CORRIDOR-A',
            defaults={
                'name': 'Ring Road High-Speed Elevated Corridor Expansion (Phase 4)',
                'organization': org,
                'contractor': contractor1,
                'project_manager': users[1],
                'budget': Decimal('320000000.00'),
                'actual_spending': Decimal('85000000.00'),
                'progress': 45,
                'start_date': '2025-06-01',
                'end_date': '2027-08-31',
                'status': 'ACTIVE',
                'description': 'Widening existing 6-lane elevated viaduct to 8-lane composite deck with sound barrier walls.'
            }
        )
        ProjectMilestone.objects.get_or_create(
            project=proj1,
            milestone_title='Phase 1: Substructure Piling & Pier Cap Erection (120 Piers)',
            defaults={
                'due_date': '2026-04-30',
                'is_completed': True,
                'completed_date': '2026-04-25',
                'weight_percentage': 30,
            }
        )
        ProjectMilestone.objects.get_or_create(
            project=proj1,
            milestone_title='Phase 2: Precast Segmental Box Girder Launching',
            defaults={
                'due_date': '2026-11-30',
                'is_completed': False,
                'weight_percentage': 40,
            }
        )

        # 8. Fiscal Budgets & Expense Ledgers
        bud1, _ = Budget.objects.get_or_create(
            budget_code='BUD-FY-2026-2027',
            defaults={
                'title': 'Annual Municipal Infrastructure Capital & Maintenance Budget FY2026-27',
                'budget_type': 'CAPITAL_PROJECT',
                'fiscal_year': 2026,
                'organization': org,
                'department': dept_highways,
                'allocated_amount': Decimal('1500000000.00'),
                'spent_amount': Decimal('485000000.00'),
                'notes': 'Consolidated budgetary allocation for highway resurfacing, bridge structural rehabilitation, and public assets.'
            }
        )
        alloc1, _ = BudgetAllocation.objects.get_or_create(
            budget=bud1,
            category_name='Arterial Road Pavement Resurfacing & Milling',
            defaults={
                'allocated_amount': Decimal('450000000.00'),
                'spent_amount': Decimal('180000000.00'),
            }
        )
        alloc2, _ = BudgetAllocation.objects.get_or_create(
            budget=bud1,
            category_name='Bridge Bearings, Expansion Joints & Structural Retrofits',
            defaults={
                'allocated_amount': Decimal('320000000.00'),
                'spent_amount': Decimal('95000000.00'),
            }
        )

        # Expenses
        Expense.objects.get_or_create(
            expense_id='EXP-2026-0081',
            defaults={
                'asset': a1,
                'project': proj1,
                'contractor': contractor2,
                'category': 'MATERIALS',
                'amount': Decimal('14500000.00'),
                'expense_date': '2026-02-10',
                'invoice_number': 'IOCL-DEL-9921',
                'description': 'Polymer Modified Bitumen (PMB-40) Bulk Supply Invoice',
                'approval_status': 'APPROVED',
                'approved_by': users[0],
            }
        )
        Expense.objects.get_or_create(
            expense_id='EXP-2026-0094',
            defaults={
                'asset': a2,
                'project': proj1,
                'contractor': contractor1,
                'category': 'CONTRACTOR',
                'amount': Decimal('28500000.00'),
                'expense_date': '2026-02-28',
                'invoice_number': 'LNT-BILL-4410',
                'description': 'Pot-PTFE Bridge Bearing Replacement Tranche 1',
                'approval_status': 'APPROVED',
                'approved_by': users[0],
            }
        )

        # 9. Maintenance Programs & Work Orders
        plan1, _ = MaintenancePlan.objects.get_or_create(
            maintenance_code='MP-RING-2026',
            defaults={
                'title': 'Annual Preventive Asphalt Micro-Surfacing & Joint Resealing',
                'maintenance_type': 'PREVENTIVE',
                'priority': 'HIGH',
                'asset': a1,
                'assigned_team': team_rapid,
                'contractor': contractor2,
                'start_date': '2026-01-10',
                'cost': Decimal('18500000.00'),
                'status': 'IN_PROGRESS',
                'notes': 'Systematic cold milling, crack potting, and 30mm Stone Matrix Asphalt (SMA) wearing course overlay.'
            }
        )
        MaintenanceActionLog.objects.get_or_create(
            maintenance_plan=plan1,
            step_description='Cold Milling & Tack Coat Application on Km 2.0 to 4.5',
            defaults={
                'technician': users[1],
                'notes': 'Sub-base inspected. Zero rutting detected beneath milled binder course.'
            }
        )

        wo1, _ = WorkOrder.objects.get_or_create(
            workorder_id='WO-2026-0491',
            defaults={
                'title': 'Emergency Pothole Patching & Thermoplastic Striping - AIIMS Underpass',
                'priority': 'HIGH',
                'status': 'IN_PROGRESS',
                'asset': a1,
                'location': locations[0],
                'assigned_employee': emp1,
                'contractor': contractor2,
                'estimated_cost': Decimal('450000.00'),
                'actual_cost': Decimal('380000.00'),
                'due_date': '2026-03-05',
                'description': 'Milling out localized 80mm surface failure and infilling with warm mix asphalt with vibro-roller compaction.'
            }
        )
        WorkOrderTask.objects.get_or_create(
            work_order=wo1,
            task_title='Deploy traffic diversion safety cones and reflective arrow signage (IRC:SP:55 compliance).',
            defaults={
                'is_completed': True,
                'hours_spent': Decimal('1.5'),
                'technician_name': 'Anita Deshmukh',
            }
        )
        WorkOrderTask.objects.get_or_create(
            work_order=wo1,
            task_title='Saw-cut square edges around pothole defect and clean cavity with compressed air.',
            defaults={
                'is_completed': False,
                'hours_spent': Decimal('2.0'),
                'technician_name': 'Rajesh Sharma',
            }
        )

        # 10. Inspections, Road Defects & Conditions
        insp1, _ = Inspection.objects.get_or_create(
            inspection_id='INSP-2026-0112',
            defaults={
                'inspection_type': 'STRUCTURAL',
                'status': 'COMPLETED',
                'asset': a2,
                'inspector': users[2],
                'inspection_date': '2026-02-10',
                'condition_score': 95,
                'findings': 'Magnetic flux leakage (MFL) testing on 64 stay cables showed zero wire breaks. Cable damping within design resonance threshold.',
                'recommendations': 'Maintain bi-annual cable tension re-calibration cycle.'
            }
        )
        InspectionChecklistItem.objects.get_or_create(
            inspection=insp1,
            item_title='Main Pylon Base Anchor Tensile Stress Verification',
            defaults={
                'is_satisfactory': True,
                'score_1_to_10': 9,
                'comments': 'All tie-down rods sound. Measured 482 MPa (Limit: 650 MPa).'
            }
        )
        InspectionChecklistItem.objects.get_or_create(
            inspection=insp1,
            item_title='Expansion Joint Elastomeric Seal Integrity',
            defaults={
                'is_satisfactory': True,
                'score_1_to_10': 9,
                'comments': 'Debris cleaned from finger joints. Gap 142mm.'
            }
        )

        RoadDefect.objects.get_or_create(
            road=a1.road_extension,
            defect_type='POTHOLE',
            defaults={
                'severity': 'MEDIUM',
                'chainage_km': Decimal('3.42'),
                'description': 'Water ingress induced surface breakup near drain grate.'
            }
        )

        ConditionLog.objects.get_or_create(
            asset=a1,
            recorded_date='2026-02-20',
            defaults={
                'condition_score': 88,
                'condition_category': 'GOOD',
                'structural_index': 90,
                'operational_index': 85,
                'safety_index': 92,
                'assessor': users[2],
                'notes': 'Routine condition log recorded post monsoon audit.'
            }
        )
        DeteriorationModel.objects.get_or_create(
            asset_type='ROAD',
            defaults={
                'expected_lifecycle_years': 25,
                'annual_decay_rate_pct': Decimal('3.20'),
                'heavy_load_multiplier': Decimal('1.40'),
                'severe_climate_multiplier': Decimal('1.25'),
                'description': 'Standard asphalt deterioration model with monsoon heavy vehicle traffic degradation curve.'
            }
        )
        DeteriorationModel.objects.get_or_create(
            asset_type='BRIDGE',
            defaults={
                'expected_lifecycle_years': 100,
                'annual_decay_rate_pct': Decimal('0.85'),
                'heavy_load_multiplier': Decimal('1.20'),
                'severe_climate_multiplier': Decimal('1.15'),
                'description': 'Cable-stayed and prestressed concrete bridge degradation profile.'
            }
        )
        InfrastructureHealthIndex.objects.get_or_create(
            asset=a1,
            defaults={
                'pavement_condition_index': Decimal('84.00'),
                'structural_integrity_rating': Decimal('90.00'),
                'risk_priority_number': 120,
                'expected_remaining_service_life_years': Decimal('22.5'),
            }
        )
        InfrastructureHealthIndex.objects.get_or_create(
            asset=a2,
            defaults={
                'bridge_condition_index': Decimal('93.50'),
                'structural_integrity_rating': Decimal('97.00'),
                'risk_priority_number': 45,
                'expected_remaining_service_life_years': Decimal('92.0'),
            }
        )

        # 11. Incidents & Rapid Dispatch
        inc1, _ = Incident.objects.get_or_create(
            incident_id='INC-2026-0044',
            defaults={
                'title': 'Sudden Stormwater Drain Collapse & Surface Cavity Formation',
                'incident_type': 'ROAD_HAZARD',
                'severity': 'HIGH',
                'status': 'DISPATCHED',
                'asset': a1,
                'location': locations[0],
                'reported_by': users[5],
                'emergency_crew': team_rapid,
                'description': 'Underground culvert joint dislocation created 1.5m deep road void during flash rains. Traffic slowed.',
                'estimated_damage_cost': Decimal('650000.00'),
            }
        )
        IncidentDispatchLog.objects.get_or_create(
            incident=inc1,
            responder_name='Inspector Anita Deshmukh & Emergency Crew Alpha',
            defaults={
                'action_taken': 'Barricaded outer 2 lanes with water-filled jersey barriers. Trench box deployed for shoring stabilization.'
            }
        )

        # 12. Warehouses, Materials & Inventory
        wh1, _ = Warehouse.objects.get_or_create(
            code='WH-CENTRAL-01',
            defaults={
                'name': 'Central Civil Materials Depot & Bitumen Yard',
                'organization': org,
                'location': locations[0],
                'capacity_sqm': Decimal('15000.00'),
                'manager': users[1],
                'contact_phone': '+91-11-23348050',
                'address': 'Ring Road Maintenance Yard, Ansari Nagar, New Delhi',
                'is_active': True,
            }
        )
        cat_pave, _ = InventoryCategory.objects.get_or_create(code='CAT-MAT-PAVE', defaults={'name': 'Bituminous & Pavement Materials'})
        cat_steel, _ = InventoryCategory.objects.get_or_create(code='CAT-MAT-STEEL', defaults={'name': 'Structural Steel & Rebar'})
        cat_signs, _ = InventoryCategory.objects.get_or_create(code='CAT-MAT-SIGN', defaults={'name': 'Safety Barriers & Road Furniture'})

        sp1, _ = SparePart.objects.get_or_create(
            part_number='MAT-PMB-40',
            defaults={
                'name': 'Polymer Modified Bitumen Grade 40 (PMB-40)',
                'category': cat_pave,
                'unit_of_measure': 'TON',
                'unit_cost': Decimal('62000.00'),
                'minimum_reorder_level': 20,
                'maximum_stock_level': 200,
                'lead_time_days': 5,
                'manufacturer': 'Indian Oil Corp',
                'barcode': '8901234567890',
            }
        )
        sp2, _ = SparePart.objects.get_or_create(
            part_number='MAT-CRASH-W',
            defaults={
                'name': 'Galvanized W-Beam Metal Crash Barrier (3.81m Section)',
                'category': cat_signs,
                'unit_of_measure': 'PCS',
                'unit_cost': Decimal('4850.00'),
                'minimum_reorder_level': 50,
                'maximum_stock_level': 1000,
                'lead_time_days': 7,
                'manufacturer': 'Tata Steel Ltd',
                'barcode': '8909876543210',
            }
        )

        StockItem.objects.get_or_create(
            warehouse=wh1,
            spare_part=sp1,
            defaults={'quantity_on_hand': 65, 'quantity_reserved': 15, 'aisle_bin_location': 'Yard Bay 4'}
        )
        StockItem.objects.get_or_create(
            warehouse=wh1,
            spare_part=sp2,
            defaults={'quantity_on_hand': 280, 'quantity_reserved': 40, 'aisle_bin_location': 'Rack B-12'}
        )

        StockMovementLedger.objects.get_or_create(
            movement_number='MOV-2026-0019',
            defaults={
                'movement_type': 'INWARD',
                'spare_part': sp1,
                'destination_warehouse': wh1,
                'quantity': 50,
                'unit_price': Decimal('62000.00'),
                'total_cost': Decimal('3100000.00'),
                'moved_by': users[1],
                'notes': 'Direct tanker delivery received and density tested.'
            }
        )

        pr1, _ = PurchaseRequisition.objects.get_or_create(
            pr_number='PR-2026-0038',
            defaults={
                'title': 'Emergency Restocking of Cold Asphalt Mix and Road Reflectors',
                'requesting_department': dept_highways,
                'warehouse_destination': wh1,
                'requested_by': users[1],
                'approver': users[4],
                'status': 'APPROVED',
                'priority': 'HIGH',
                'total_estimated_cost': Decimal('970000.00'),
                'justification': 'Essential for monsoon rapid pothole emergency patch repairs.'
            }
        )
        PurchaseRequisitionItem.objects.get_or_create(
            requisition=pr1,
            spare_part=sp2,
            defaults={'quantity': 200, 'estimated_unit_cost': Decimal('4850.00'), 'total_amount': Decimal('970000.00')}
        )

        # 13. Schedules & Preventive Planner
        sch1, _ = AssetSchedule.objects.get_or_create(
            schedule_code='SCH-BRG-CABLE-Q',
            defaults={
                'title': 'Quarterly Ultrasonic Cable Deflection & Tension Calibration',
                'schedule_type': 'STATUTORY_AUDIT',
                'asset': a2,
                'organization': org,
                'department': dept_highways,
                'assigned_team': team_bridge,
                'assigned_contractor': contractor1,
                'frequency': 'QUARTERLY',
                'start_date': '2026-01-01',
                'next_due_date': timezone.now().date() + timedelta(days=25),
                'auto_generate_workorder': True,
                'is_active': True,
                'description': 'Laser alignment and load cell calibration across all 128 stay anchor heads.'
            }
        )
        ScheduledEventExecution.objects.get_or_create(
            schedule=sch1,
            scheduled_date=timezone.now().date() + timedelta(days=25),
            defaults={'status': 'PENDING', 'assigned_to': users[2]}
        )

        # 14. Support Tickets & Citizen Grievances
        tkt1, _ = SupportTicket.objects.get_or_create(
            ticket_number='TKT-2026-0812',
            defaults={
                'subject': 'Large Pothole Hazard near AIIMS Flyover Northbound Descent',
                'category': 'POTHOLE_HAZARD',
                'priority': 'HIGH',
                'status': 'IN_PROGRESS',
                'asset': a1,
                'location': locations[0],
                'reporter_name': 'Dr. Alok Verma',
                'reporter_email': 'alok.verma@aiims.edu',
                'reporter_phone': '+91-9810012345',
                'is_citizen_complaint': True,
                'assigned_to': users[1],
                'assigned_department': dept_highways,
                'description': 'Deep crater in middle lane causing severe vehicle jolts and traffic backlog during morning peak hours.'
            }
        )
        TicketComment.objects.get_or_create(
            ticket=tkt1,
            author=users[1],
            defaults={
                'author_name': 'Rajesh Sharma (Chief Engineer)',
                'comment': 'Work Order WO-2026-0491 dispatched. Asphalt patching scheduled tonight at 23:00 hrs during zero-traffic window.',
                'is_internal_note': False
            }
        )

        SLAPolicy.objects.get_or_create(
            priority='CRITICAL',
            defaults={'name': 'Disaster & Critical Structural Hazard Response SLA', 'response_time_hours': 2, 'resolution_time_hours': 12, 'escalation_email': 'emergency@infraflowx.gov'}
        )
        SLAPolicy.objects.get_or_create(
            priority='HIGH',
            defaults={'name': 'High Priority Road Surface & Pothole SLA', 'response_time_hours': 6, 'resolution_time_hours': 24, 'escalation_email': 'highways@infraflowx.gov'}
        )
        SLAPolicy.objects.get_or_create(
            priority='MEDIUM',
            defaults={'name': 'Standard Maintenance Service SLA', 'response_time_hours': 24, 'resolution_time_hours': 72, 'escalation_email': 'maintenance@infraflowx.gov'}
        )

        # 15. Documents & CAD Blueprints
        doc_cat_cad, _ = DocumentCategory.objects.get_or_create(code='CAT-CAD', defaults={'name': 'Engineering Blueprints & CAD Drawings'})
        doc_cat_spec, _ = DocumentCategory.objects.get_or_create(code='CAT-SPEC', defaults={'name': 'Technical Specifications & Design Criteria'})

        d1, _ = Document.objects.get_or_create(
            doc_number='DWG-YAMUNA-STR-001',
            defaults={
                'title': 'Signature Bridge General Structural Elevation & Pylon Anchorage Drawing',
                'category': doc_cat_cad,
                'asset': a2,
                'organization': org,
                'current_version': '3.2',
                'is_blueprint': True,
                'confidentiality': 'RESTRICTED',
                'status': 'APPROVED',
                'uploaded_by': users[1],
                'tags': 'bridge, structural, pylon, cad, signature',
                'description': 'Full architectural and structural drawing set for 154m bow-shaped steel pylon and stay cable layout.'
            }
        )
        BlueprintMetadata.objects.get_or_create(
            document=d1,
            defaults={
                'drawing_number': 'DWG-SB-STR-EL-01',
                'scale_ratio': '1:200',
                'sheet_size': 'A0',
                'cad_software': 'AutoCAD 2024 / Tekla Structures',
                'engineer_signoff_name': 'Prof. J. Schlaich, Dr. Ing. (Consultant)',
                'approval_date': '2018-09-15',
            }
        )

        # 16. Report Templates
        ReportTemplate.objects.get_or_create(
            code='RPT-ASSET-REG',
            defaults={
                'title': 'Master Infrastructure Asset Registry & Valuation Export',
                'module': 'ASSETS',
                'default_format': 'CSV',
                'description': 'Full tabular export of physical infrastructure assets, condition scores, acquisition costs, and GIS locations.'
            }
        )
        ReportTemplate.objects.get_or_create(
            code='RPT-WO-BACKLOG',
            defaults={
                'title': 'Work Order Performance & Maintenance Backlog Audit',
                'module': 'WORKORDERS',
                'default_format': 'CSV',
                'description': 'Operational maintenance tickets, priority distributions, actual cost vs budget variances, and technician assignments.'
            }
        )
        ReportTemplate.objects.get_or_create(
            code='RPT-INSP-AUDIT',
            defaults={
                'title': 'Structural Health & Inspection Audit Log',
                'module': 'INSPECTIONS',
                'default_format': 'CSV',
                'description': 'Engineering inspection results, NDT ultrasound scores, pavement condition ratings, and inspector sign-offs.'
            }
        )
        ReportTemplate.objects.get_or_create(
            code='RPT-EXPENSE-FIN',
            defaults={
                'title': 'Fiscal Expense Disbursements & Invoice Ledger',
                'module': 'FINANCIALS',
                'default_format': 'CSV',
                'description': 'Disbursed public works expenditure breakdown against allocated municipal budget line items.'
            }
        )

        # 17. Executive KPI Targets
        KPITarget.objects.get_or_create(
            metric_key='KPI_ASSET_UPTIME',
            defaults={
                'name': 'Operational Asset Availability Rate',
                'target_value': Decimal('95.00'),
                'warning_threshold': Decimal('90.00'),
                'critical_threshold': Decimal('85.00'),
                'unit': '%',
                'current_actual_value': Decimal('92.40'),
                'is_higher_better': True,
                'description': 'Percentage of critical road, bridge, and public facility network operating with zero closures.'
            }
        )
        KPITarget.objects.get_or_create(
            metric_key='KPI_WO_SLA',
            defaults={
                'name': 'Work Order On-Time SLA Resolution Rate',
                'target_value': Decimal('90.00'),
                'warning_threshold': Decimal('80.00'),
                'critical_threshold': Decimal('70.00'),
                'unit': '%',
                'current_actual_value': Decimal('88.50'),
                'is_higher_better': True,
                'description': 'Percentage of corrective maintenance tickets resolved strictly within regulatory SLA windows.'
            }
        )

        # 18. Audit & Notification log triggers
        log_audit_event(
            action='SYSTEM',
            module='system',
            object_id=str(uuid.uuid4()),
            description='InfraFlowX Enterprise Platform Demonstration Data Seed Completed Successfully.',
            user=admin_user
        )
        send_notification(
            recipient=admin_user,
            title='Demo Data Population Complete',
            message='InfraFlowX 27 modular apps successfully seeded with real-world infrastructure data.',
            notification_type='SYSTEM',
            priority='HIGH'
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated full InfraFlowX enterprise demonstration data!'))
