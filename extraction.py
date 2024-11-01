import dotenv
from extract.api_request import ApiRequest
from datetime import datetime, timedelta
import pandas as pd
import os
import random

dotenv.load_dotenv(dotenv.find_dotenv('.env'))

API_KEY_FINDWORK = os.getenv("FINDWORK_API_KEY")

def fetch_remotive_jobs():
    """Fetches and transforms jobs from the Remotive API."""
    remotive_request = ApiRequest(
        url='https://remotive.com/api/remote-jobs',
        params={}
    )
    data = remotive_request.make_request()
    if data:
        jobs = data.get('jobs', [])
        return transform_remotive_jobs(jobs)
    return []

def fetch_remoteok_jobs():
    """Fetches and transforms jobs from the RemoteOK API."""
    remoteok_request = ApiRequest(
        url='https://remoteok.com/api',
        params={}
    )
    data = remoteok_request.make_request()
    if data:
        jobs = data[1:]  # Skipping the first entry if it's metadata
        return transform_remoteok_jobs(jobs)
    return []

def fetch_findwork_jobs():
    """Fetches and transforms jobs from the Findwork API."""
    if not API_KEY_FINDWORK:
        raise ValueError("FINDWORK_API_KEY is missing. Check your .env file.")

    findwork_request = ApiRequest(
        url='https://findwork.dev/api/jobs/',
        header={"Authorization": f"Token {API_KEY_FINDWORK}"},
        params={"date_posted": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")}
    )
    data = findwork_request.make_request()
    if data:
        jobs = data.get('results', [])
        return [create_job_entry(job) for job in jobs]
    return []

def transform_remotive_jobs(jobs):
    """Transforms the Remotive jobs data to a consistent format."""
    for job in jobs:
        job['location'] = job.pop('candidate_required_location', '')
        job['date'] = job.pop('publication_date', '')
        job['salary_range'] = job.pop("salary", '')
    return jobs

def transform_remoteok_jobs(jobs):
    """Transforms the RemoteOK jobs data to a consistent format."""
    for job in jobs:
        job['position'] = job.pop('title', '')
        job['company_name'] = job.pop('company', '')
        job['job_type'] = 'Remote'
        
        salary_min = job.get('salary_min', '')
        salary_max = job.get('salary_max', '')
        job['salary_range'] = f"{salary_min} - {salary_max}" if salary_min and salary_max else ''
    return jobs

def create_job_entry(job):
    """Creates a job entry in a standardized format."""
    salary_min = random.randint(5000, 25000)
    salary_max = random.randint(salary_min, 50000)
    return {
        'title': job.get('role'),
        'company_name': job.get('company_name'),
        'url': job.get('url'),
        'job_type': job.get('employment_type'),
        'location': job.get('location'),
        'date': job.get('date_posted'),
        'salary_range': f"{salary_min} - {salary_max}"
    }

if __name__ == '__main__':
    pass