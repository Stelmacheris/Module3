# Job Application System

This repository consist of project to fetc data from API's, transform it and load to cloud database. All flow is being done with Apache airflow

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker

## Installation Guide

### 1. Clone the Repository

Start by cloning this repository to your local machine using:

```bash
https://github.com/TuringCollegeSubmissions/martstelm-DE3v2.1.5.git
martstelm-DE3v2.1.5.git
```

### 2. Build docker image

```bash
docker build -t <image_name> .
```

### 3. Configure Environment Variables

Create a .env file in the app directory of your project and add the following environment variables to configure your database connection and other attributes for Apache Airflow:

```env
AIRFLOW_UID=<AIRFLOW_UID>
AIRFLOW__CORE__EXECUTOR=<AIRFLOW__CORE__EXECUTOR>
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=<AIRFLOW__DATABASE__SQL_ALCHEMY_CONN>
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=<AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION>
AIRFLOW__CORE__LOAD_EXAMPLES=<AIRFLOW__CORE__LOAD_EXAMPLES>
AIRFLOW__API__AUTH_BACKENDS=<AIRFLOW__API__AUTH_BACKENDS>
AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK=<AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK>
FINDWORK_API_KEY=<FINDWORK_API_KEY>
DB_USER = <DB_USER>
DB_PASSWORD = <DB_PASSWORD>
DB_DATABASE = <DB_DATABASE>
DB_HOST =<DB_HOST>
DB_PORT = <DB_PORT>
```

### 4. Run application

```bash
docker compose up -d
```

### 5. Verify the Import

```sql
SELECT *
FROM public.job_statistics
LIMIT 10;
```

## Usage

You can now use pgAdmin or any other PostgreSQL client to connect to the `<DB_DATABASE>` database and run queries, generate reports, or perform analysis.
