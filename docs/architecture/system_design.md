# InfraFlowX - Enterprise Architecture & System Design Document

## 1. Architectural Overview
InfraFlowX is an enterprise-grade infrastructure and physical asset lifecycle management platform designed for municipal governments, transportation departments, public utility authorities, and large-scale facility management organizations.

### Core Principles:
- **Clean Django MVT Modular Architecture**: 27 decoupled domain apps operating under unified authentication and organizational multi-tenancy.
- **SQLite Single-File Robustness**: Zero-configuration production SQLite database engine with atomic transactions.
- **Mathematical & Structural Engineering Rigor**: Built-in deterministic calculation engines implementing ASTM, AASHTO, FHWA, IEEE, and ISO international standards.
- **Cryptographic Auditability**: SHA-256 Merkle hash chains ensuring tamper-evident operational logs.
- **Spatial Multi-Layer GIS**: Native Leaflet.js mapping with GeoJSON corridor topology and bounding box geospatial indexing.

---

## 2. Domain App Decomposition
The platform is organized into 27 discrete domain apps:
1. **accounts**: Identity, NIST password security, TOTP multi-factor authentication, session management.
2. **organizations**: Multi-tenant isolation, organizational hierarchical charts, subscription tier quotas.
3. **employees**: Labor rate burdens, skill matrices, professional licensure tracking.
4. **assets**: Unified asset registry, ISO 55000 Business Risk Exposure (BRE), MACRS depreciation.
5. **roads**: ASTM D6433 Pavement Condition Index (PCI), AASHTO Structural Number (SN), HDM-4 roughness.
6. **bridges**: FHWA Sufficiency Rating (SR), HEC-18 scour hydraulics, AASHTO LRFR load rating.
7. **buildings**: Facility Condition Index (FCI), ASHRAE Energy Utilization Index (EUI), IBC egress compliance.
8. **facilities**: IEEE 493 Gold Book MTBF/MTTR, k-out-of-n redundancy, Hazen-Williams pipe hydraulics.
9. **locations**: Vincenty geodesic distance, R-tree spatial indexing, ray-casting point-in-polygon tests.
10. **inspections**: Dynamic QA/QC checklist scoring, UAV drone photogrammetry telemetry, ASTM NDT testing.
11. **conditions**: 1D Kalman sensor fusion, Markov deterioration transition matrices.
12. **maintenance**: Exponential RUL prediction, Clarke-Wright heuristic crew routing dispatch.
13. **workorders**: Municipal SLA business hours countdown, parametric RSMeans unit cost estimation.
14. **projects**: ANSI/EIA-748 Earned Value Management (EVM), Critical Path Method (CPM) scheduling.
15. **contractors**: Competitive bid tab anomaly detection, OSHA TRIR, AIA G702 retainage accounting.
16. **budgets**: Holt-Winters CIP multi-year forecasting, 0/1 Knapsack capital budget optimization.
17. **expenses**: Receipt OCR reconciliation, multi-tier delegation of authority (DOA) workflows.
18. **incidents**: 5-Whys root cause analysis, Ishikawa fishbone synthesis, FEMA NIMS ICS mobilization.
19. **documents**: CAD/DXF metadata extraction, semantic versioning, SHA-256 digital fingerprinting.
20. **inventory**: FIFO/FEFO lotted inventory depletion, GS1-128 barcode / EPC Gen2 RFID tracking.
21. **schedules**: Burgess resource leveling, 24/7 DuPont rotating shift generators.
22. **notifications**: Multi-channel alert matrix, automated escalation ladders, HMAC signed webhooks.
23. **analytics**: IoT Z-score anomaly detection, Moran's I spatial autocorrelation clustering.
24. **reports**: Printable HTML executive reports, FEMA Project Worksheet cost schedules.
25. **support**: BM25 technical SOP search, customer satisfaction (CSAT) scoring.
26. **permissions**: Attribute-Based Access Control (ABAC), row-level security (RLS) scoping.
27. **audit**: Tamper-evident Merkle hash chains, SOC 2 Type II compliance evidence packages.
