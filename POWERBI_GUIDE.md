# Power BI Integration Guide

## Step 1 — Export CSV from Flask API

Once your Flask app is running, export each dataset:

```
GET http://localhost:5000/export/Patients
```

This downloads `Patients_export.csv` — import it directly into Power BI.

---

## Step 2 — Import into Power BI Desktop

1. Open Power BI Desktop
2. Click **Get Data → Text/CSV**
3. Select the exported CSV file
4. Click **Transform Data** to clean before loading

---

## Step 3 — Connect Live via Web API (optional)

1. Click **Get Data → Web**
2. Enter one of these URLs:

```
http://localhost:5000/analytics/conditions
http://localhost:5000/analytics/admission_types
http://localhost:5000/analytics/insurance
http://localhost:5000/analytics/test_results
http://localhost:5000/analytics/monthly_admissions
http://localhost:5000/analytics/top_doctors
```

3. Power BI will parse the JSON automatically

---

## Step 4 — Recommended Dashboards

| Visual Type   | X-Axis / Legend        | Y-Axis / Values            | Insight                        |
|---------------|------------------------|----------------------------|--------------------------------|
| Bar Chart     | Medical Condition      | Count of Patients          | Most common conditions         |
| Pie Chart     | Admission Type         | Count                      | Urgent vs Emergency vs Elective|
| Line Chart    | Admission Month        | Count of Admissions        | Admission trends over time     |
| Bar Chart     | Insurance Provider     | Avg Billing Amount         | Billing by insurer             |
| Donut Chart   | Test Results           | Count                      | Normal/Abnormal/Inconclusive   |
| Table         | Doctor                 | Patient Count, Avg Billing | Top doctors                    |
| KPI Card      | -                      | Total Patients             | 55,500 patients                |
| KPI Card      | -                      | Avg Billing Amount         | Overall avg billing            |
| KPI Card      | -                      | Avg Length of Stay         | Avg days per admission         |

---

## Step 5 — Publish

1. Click **File → Publish → Publish to Power BI**
2. Sign in with your Microsoft account (free)
3. Dashboard is now accessible online and shareable
