# Healthcare-Data-Platform

This project is a **scalable Electronic Health Records (EHR) Simulation Platform** designed for healthcare analytics, interoperability experimentation, and real-time data insights. It leverages a robust modern stack—**Python, R, Flask, Docker, Spark, Hadoop, MongoDB, AWS EC2, Power BI**—to enable ETL automation, distributed processing, cloud-native deployment, and advanced statistical validation.

## 🚀 Features

- **Modular RESTful APIs:**  
  Flask-based APIs for data ingestion, access, and management of simulated EHR datasets.

- **Containerized ETL Workflows:**  
  Automated data extraction, transformation, and loading using Dockerized pipelines for consistent, scalable processing.

- **Distributed Data Processing:**  
  Integrated **Apache Spark** and **Hadoop** engines for big data computation, supporting large-volume healthcare analytics and fast query performance.

- **Data Storage:**  
  Utilizes **MongoDB** for storing semi-structured clinical data, supporting flexible schema evolution.

- **Cloud Deployment:**  
  Easily deployed and orchestrated on **AWS EC2**, allowing horizontal scaling and robust infrastructure for production use cases.

- **Real-Time Dashboards:**  
  Live data visualization and KPI monitoring powered by **Power BI**, enabling users to monitor operational and clinical metrics in real time.

- **Integrated R-Python Workflows:**  
  Seamlessly combines R and Python processes for advanced statistical validation, data science, and automation—vital for healthcare research and regulatory requirements.

## 🏗️ Architecture

| Component             | Tech Stack                           | Description                                                    |
|-----------------------|--------------------------------------|----------------------------------------------------------------|
| API Layer             | Flask, REST API                      | Data access and control endpoints                              |
| ETL/Data Processing   | Docker, Spark, Hadoop                | Scalable, reproducible workflows for simulation and analytics  |
| Data Layer            | MongoDB                              | Flexible NoSQL storage for EHR data                            |
| Cloud Deployment      | AWS EC2                              | Cloud hosting and orchestration                                |
| Analytics & BI        | Power BI                             | Rich, real-time dashboarding                                   |
| Statistical Analysis  | R, Python, R-Python integration      | Automation and model validation in multi-language pipelines    |

## ⚙️ Getting Started

### Prerequisites

- Docker/Docker Compose
- Python (3.8+)
- R (with required packages)
- AWS account (for EC2 deployment)
- Access to Power BI

### Quick Start

```bash
# Step 1: Clone repository
git clone 
cd healthcare-data-platform

# Step 2: Build and launch containers
docker-compose up --build

# Step 3: Setup environment variables (see .env.example)
```

## 🌐 Use Cases

- Healthcare data simulation and benchmarking
- ETL automation for clinical data warehouses
- High-throughput healthcare analytics and research
- Rapid prototyping and testing of health informatics models
- Real-time monitoring and KPI tracking in health operations

