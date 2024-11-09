from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os
from extraction import fetch_findwork_jobs, fetch_remoteok_jobs, fetch_remotive_jobs
from transformation import create_df, clean_df, create_statistic
from load_to_database import insert_to_database

with DAG(
    'api_data_processing',
    description='A DAG for extracting, concatenating, and processing API data',
    schedule_interval='0 0 * * *',
    start_date=datetime(2024, 10, 1),
    end_date=datetime(2024, 12, 1),
    catchup=False,
    params={}
) as dag:

    extract_data_api_1 = PythonOperator(
        task_id='fetch_findwork_jobs',
        python_callable=fetch_findwork_jobs,
        params={}
    )

    extract_data_api_2 = PythonOperator(
        task_id='fetch_remoteok_jobs',
        python_callable=fetch_remoteok_jobs,
        params={}
    )

    extract_data_api_3 = PythonOperator(
        task_id='fetch_remotive_jobs',
        python_callable=fetch_remotive_jobs,
        params={}
    )

    concatenate_data = PythonOperator(
        task_id='concatenate_data',
        python_callable=create_df,
        params={}
    )

    cleaned_df = PythonOperator(
        task_id='cleaned_df',
        python_callable=clean_df,
        params={}
    )

    created_statistic = PythonOperator(
        task_id='create_statistic',
        python_callable=create_statistic,
        params={}
    )

    inserted_to_database = PythonOperator(
        task_id='insert_to_database',
        python_callable=insert_to_database,
        params={}
    )

[extract_data_api_1, extract_data_api_2, extract_data_api_3] >> concatenate_data >> cleaned_df >> created_statistic >> inserted_to_database
