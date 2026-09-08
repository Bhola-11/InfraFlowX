# InfraFlowX

**Enterprise Infrastructure & Asset Lifecycle Management Platform**

InfraFlowX is a centralized infrastructure and physical asset lifecycle management platform architected for municipal governments, public utility authorities, transportation departments, and private engineering operators.

---

## Table of Contents
1. [Overview & Architecture](#overview--architecture)
2. [Key Features & 27 Domain Apps](#key-features--27-domain-apps)
3. [Installation](#installation)
4. [Build & Database Setup](#build--database-setup)
5. [Run Instructions](#run-instructions)
6. [Dependencies](#dependencies)
7. [Usage & Operational Workflows](#usage--operational-workflows)
8. [Automated Testing & Code Coverage](#automated-testing--code-coverage)
9. [License](#license)

---

## Overview & Architecture
- **Architecture**: Django Model-View-Template (MVT) with SQLite (`db.sqlite3`).
- **Codebase Volume**: 100,000+ Lines of Code across 27 decoupled domain applications.
- **Frontend Stack**: Bootstrap 5 (Dark & Elevated Theme), Leaflet.js (GIS Multi-Layer Spatial Mapping), Chart.js (Dynamic Data Visualizations).
- **Standards Compliance**: ASTM D6433 (PCI), AASHTO LRFD / SN, FHWA HEC-18 (Scour), ASHRAE Standard 100 (EUI), IEEE 493 (Reliability), ANSI/EIA-748 (Earned Value Management), NIST SP 800-63B, and FEMA NIMS ICS.

---

## Key Features & 27 Domain Apps
The platform decomposes municipal infrastructure management into 27 discrete applications:
- **`accounts`**: Identity management, NIST SP 800-63B password policy, TOTP RFC 6238 MFA.
- **`organizations`**: Multi-tenant isolation, department hierarchies, plan tier capacity quotas.
- **`employees`**: Fully burdened labor rate multipliers, skill matrices, license tracking.
- **`assets`**: Unified asset registry, ISO 55000 Business Risk Exposure (BRE), MACRS depreciation.
- **`roads`**: ASTM D6433 Pavement Condition Index (PCI), AASHTO Structural Number (SN), HDM-4 roughness.
- **`bridges`**: FHWA Sufficiency Rating (SR), HEC-18 scour hydraulics, AASHTO LRFR load rating.
- **`buildings`**: Facility Condition Index (FCI), ASHRAE Energy Utilization Index (EUI), IBC Chapter 10 life safety.
- **`facilities`**: IEEE 493 MTBF/MTTR reliability, $k$-out-of-$n$ redundancy, Hazen-Williams pipe hydraulics.
- **`locations`**: Vincenty geodesic distance, 2D spatial grid indexing, point-in-polygon geofencing.
- **`inspections`**: QA/QC checklist scoring, UAV drone photogrammetry telemetry, ASTM NDT testing.
- **`conditions`**: 1D Kalman sensor fusion filter, Markov chain deterioration transition matrices.
- **`maintenance`**: Exponential Remaining Useful Life (RUL) modeling, Clarke-Wright heuristic crew routing.
- **`workorders`**: Priority SLA business hours countdown, parametric RSMeans unit cost estimation.
- **`projects`**: ANSI/EIA-748 Earned Value Management (EVM: PV, EV, AC, CPI, SPI, EAC), Critical Path Method (CPM).
- **`contractors`**: Competitive bid tab outlier analysis, OSHA TRIR safety qualification, AIA G702 retainage escrow.
- **`budgets`**: Holt-Winters CIP multi-year expenditure forecasting, 0/1 Knapsack capital budget optimization.
- **`expenses`**: Structural receipt OCR reconciliation, 5-tier Delegation of Financial Authority (DOA) approval workflows.
- **`incidents`**: 5-Whys root cause analysis, Ishikawa fishbone breakdown, FEMA NIMS Incident Command System (ICS).
- **`documents`**: CAD / DXF layer entity metadata extraction, semantic versioning, SHA-256 digital fingerprinting.
- **`inventory`**: FIFO / FEFO lotted inventory layer depletion, GS1-128 barcode / EPC Gen2 RFID tracking.
- **`schedules`**: Burgess resource leveling, 24/7 DuPont rotating shift schedule generator.
- **`notifications`**: Multi-channel alert dispatch matrix, automated timeout escalation ladders, HMAC-SHA256 signed webhooks.
- **`analytics`**: Z-score / IQR IoT anomaly detection, Moran's I spatial autocorrelation clustering, Executive Health Index (IHI).
- **`reports`**: Standardized executive printable HTML reports, FEMA Project Worksheet (PW) disaster schedules.
- **`support`**: BM25 technical SOP search, ticket MTTR / SLA tracking, Customer Satisfaction (CSAT) analytics.
- **`permissions`**: Attribute-Based Access Control (ABAC), tenant-scoped Row-Level Security (RLS) querysets.
- **`audit`**: Cryptographic tamper-evident Merkle hash chains, SOC 2 Type II audit evidence generator.

---

## Installation

### Prerequisites
- Python 3.10+ (Recommended: Python 3.11)
- Git

### Step-by-Step Setup
```bash
# 1. Clone or extract repository
git clone https://github.com/Bhola-11/InfraFlowX.git
cd InfraFlowX

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows (PowerShell):
.env\Scripts\Activate.ps1
# On Windows (Command Prompt):
.env\Scriptsctivate.bat

# 4. Install dependencies
pip install -r requirements.txt
```

---

## Build & Database Setup
```bash
# Apply database migrations to SQLite
python manage.py makemigrations
python manage.py migrate

# Seed database with demonstration infrastructure dataset
python manage.py seed_demo_data
```

---

## Run Instructions
```bash
# Start Django development server
python manage.py runserver 127.0.0.1:8000
```
Open your web browser and navigate to: **`http://127.0.0.1:8000/`**

---

## Dependencies
Major dependencies declared in `requirements.txt` and `Pipfile`:
- `Django>=5.0.0`
- `djangorestframework>=3.14.0`
- `pytest>=8.0.0`
- `pytest-django>=4.8.0`
- `pytest-cov>=4.1.0`

---

## Usage & Operational Workflows
1. **Asset Management**: Access `/assets/`, `/roads/`, `/bridges/`, `/buildings/`, and `/facilities/` to view GIS maps, condition scores, and technical blueprints.
2. **Inspections & Work Orders**: Schedule field inspections under `/inspections/` and dispatch maintenance crews via `/workorders/`.
3. **Engineering Calculations**: Execute real-time ASTM PCI, FHWA Sufficiency Ratings, Hazen-Williams hydraulics, and EVM project metrics.
4. **Audit & Compliance**: View tamper-evident SHA-256 Merkle chains under `/audit/`.

---

## Automated Testing & Code Coverage
```bash
# Run test suite with Django test runner
python manage.py test

# Run test suite with PyTest and Coverage
pytest --cov=apps --cov-report=term-missing
```

---

## License
Proprietary — All rights reserved by InfraFlowX.
