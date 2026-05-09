# Healthcare Data Platform

A scalable, production-grade EHR analytics platform built on Flask, MongoDB, Apache Spark, Docker, AWS EC2, Power BI, and R–Python integration.

---

## Architecture

| Component             | Tech Stack                      | Description                                               |
|-----------------------|---------------------------------|-----------------------------------------------------------|
| API Layer             | Flask, REST API                 | Data access, ETL trigger, and analytics endpoints         |
| ETL / Data Processing | Docker, Spark, Pandas           | Scalable, reproducible ingestion and transformation       |
| Data Layer            | MongoDB                         | Flexible NoSQL storage for EHR records                    |
| Cloud Deployment      | AWS EC2, Docker Compose         | Cloud hosting and container orchestration                 |
| Analytics & BI        | Power BI                        | Real-time dashboarding via CSV export or live API         |
| Statistical Analysis  | R, Python, R–Python integration | Hypothesis testing, correlation, and model validation     |

---

## Dataset

55,500 patient records with 15 features:
`Name`, `Age`, `Gender`, `Blood Type`, `Medical Condition`, `Date of Admission`,
`Doctor`, `Hospital`, `Insurance Provider`, `Billing Amount`, `Room Number`,
`Admission Type`, `Discharge Date`, `Medication`, `Test Results`

---

## Project Structure

```
healthcare_platform/
├── app.py                    # Flask REST API
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── deploy_ec2.sh             # AWS EC2 deployment script
├── healthcare_dataset.csv    # Source dataset
├── etl/
│   ├── etl_pipeline.py       # Extract, Transform, Load
│   └── spark_analytics.py    # Distributed Spark analysis
├── r_analysis/
│   └── analysis.R            # R statistical analysis
└── POWERBI_GUIDE.md          # Power BI setup instructions
```

---

## Quick Start

### Run Locally

```bash
pip install -r requirements.txt
python app.py
```

### Run with Docker

```bash
docker-compose up --build
```

### Trigger ETL (load data into MongoDB)

```bash
curl -X POST http://localhost:5000/etl/run
```

---

## API Endpoints

| Method | Endpoint                          | Description                        |
|--------|-----------------------------------|------------------------------------|
| POST   | `/etl/run`                        | Run ETL pipeline                   |
| GET    | `/patients`                       | Get all patients (with filters)    |
| GET    | `/patients/<id>`                  | Get single patient                 |
| POST   | `/patients`                       | Insert new patient                 |
| PUT    | `/patients/<id>`                  | Update patient                     |
| DELETE | `/patients/<id>`                  | Delete patient                     |
| GET    | `/analytics/conditions`           | Patients by medical condition      |
| GET    | `/analytics/admission_types`      | Admission type breakdown           |
| GET    | `/analytics/insurance`            | Billing by insurance provider      |
| GET    | `/analytics/test_results`         | Test results distribution          |
| GET    | `/analytics/monthly_admissions`   | Monthly admission trends           |
| GET    | `/analytics/top_doctors`          | Top 20 doctors by patient count    |
| GET    | `/export/<collection>`            | Export collection as CSV           |

---

## Deploy on AWS EC2

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Upload project
scp -i your-key.pem -r ./healthcare_platform ubuntu@your-ec2-ip:~/

# Run deployment script
bash deploy_ec2.sh
```

---

## Statistical Analysis (R)

```bash
cd r_analysis
Rscript analysis.R
```

Outputs: ANOVA, Pearson correlation, Chi-square tests, and 3 charts saved as PNG.

---

## Distributed Analytics (Spark)

```bash
python etl/spark_analytics.py
```

Runs distributed aggregations on the full 55,500-record dataset.
