from extraction import fetch_remotive_jobs,fetch_remoteok_jobs,fetch_findwork_jobs
from transform.transform_handler import TransformHandler
from datetime import datetime, timedelta
import pandas as pd
import re

def filter_jobs_by_date(jobs, target_date):
    """Filters jobs by a specific date."""
    filtered_jobs = []
    for job in jobs:
        job_date_str = job.get('date', '')
        try:
            job_date = datetime.fromisoformat(job_date_str).date()
            if job_date == target_date:
                filtered_jobs.append(job)
        except ValueError:
            continue
    return filtered_jobs

def create_df():
    remotive_jobs = fetch_remotive_jobs()
    remoteok_jobs = fetch_remoteok_jobs()
    findwork_jobs = fetch_findwork_jobs()

    all_jobs = remotive_jobs + remoteok_jobs + findwork_jobs

    target_date = datetime.now().date() - timedelta(days=1)
    filtered_jobs = filter_jobs_by_date(all_jobs, target_date)
    jobs_df = pd.DataFrame(filtered_jobs)
    jobs_df = jobs_df[['title', 'company_name', 'url', 'job_type', 'location', 'salary_range', 'date']]
    
    return jobs_df

def clean_df():
    jobs_df = create_df()
    transfrom_handler:TransformHandler = TransformHandler(jobs_df)
    transfrom_handler.extract_date_apply('date')
    transfrom_handler.convert_to_euro_apply('salary_range')
    cleaned_df = transfrom_handler.get_df()
    return cleaned_df

def create_statistic():
    jobs_df = clean_df()
    data_engineering_df = jobs_df[jobs_df['title'].str.contains('data engineering', case=True, na=False)]
    remote_count = data_engineering_df['location'].str.contains(r'\bremote\b', case=True, na=False).sum()
    data_engineering_df = data_engineering_df.dropna(subset=['salary_range'])

    # Extract min and max salary from 'salary_range' column
    data_engineering_df[['min_salary', 'max_salary']] = data_engineering_df['salary_range'].str.extract(r'(\d+\.?\d*)€ - (\d+\.?\d*)€').astype(float)

    # Calculate min, max, average, and std for the salary range
    min_salary = float(data_engineering_df['min_salary'].min())
    max_salary = float(data_engineering_df['max_salary'].max())
    avg_salary = float(data_engineering_df[['min_salary', 'max_salary']].stack().mean())
    std_salary = float(data_engineering_df[['min_salary', 'max_salary']].stack().std())

    yesterday = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday.strftime('%Y-%m-%d')

    statsitics = {
    'date': yesterday_date,
    'data_engineering_job_count': len(data_engineering_df),
    'data_engineering_count': remote_count,
    'minimum_salary': round(min_salary, 2),
    'maximum_salary': round(max_salary, 2),
    'average_salary': round(avg_salary, 2),
    'standard_deviation': round(std_salary, 2)
    }
    statsitics_df = pd.DataFrame([statsitics])
    return statsitics_df

if __name__ == '__main__':
    clean_df()