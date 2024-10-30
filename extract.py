import asyncio
import aiohttp
import dotenv
from extract.api_request import ApiRequest  # Assuming async compatibility
import json
from datetime import datetime, timedelta
import pandas as pd
import os
import aiohttp
import random

dotenv.load_dotenv(dotenv.find_dotenv('.env'))

API_KEY_FINDWORK = os.getenv("FINDWORK_API_KEY")

async def fetch_and_transform_jobs(api_request: ApiRequest, transform_function, response_index=None, result_key=None):
    data = await api_request.async_make_request()
    if data:
        if response_index is not None:
            data = data[response_index:]
        if result_key:
            data = data.get(result_key, [])
        return transform_function(data)
    return []

def transform_remotive_jobs(jobs):
    for job in jobs:
        job['location'] = job.pop('candidate_required_location', '')
        job['date'] = job.pop('publication_date', '')
        job['salary_range'] = job.pop("salary", '')
    return jobs

def transform_remoteok_jobs(jobs):
    for job in jobs:
        job['position'] = job.pop('title', '')
        job['company_name'] = job.pop('company', '')
        job['job_type'] = 'Remote'
        
        salary_min = job.get('salary_min', '')
        salary_max = job.get('salary_max', '')
        job['salary_range'] = f"{salary_min} - {salary_max}" if salary_min and salary_max else ''
    return jobs

def create_job_entry(job):
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

def filter_jobs_by_date(jobs, target_date):
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

async def main():
    if not API_KEY_FINDWORK:
        logger.error("FINDWORK_API_KEY is missing. Check your .env file.")
        return

    remotive_request = ApiRequest(
        url='https://remotive.com/api/remote-jobs',
        params={}
    )
    remoteok_request = ApiRequest(
        url='https://remoteok.com/api',
        params={}
    )
    findwork_request = ApiRequest(
        url='https://findwork.dev/api/jobs/',
        header={"Authorization": f"Token {API_KEY_FINDWORK}"},
        params={"date_posted": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")}
    )

    remotive_jobs, remoteok_jobs, findwork_jobs = await asyncio.gather(
        fetch_and_transform_jobs(remotive_request, transform_remotive_jobs, result_key='jobs'),
        fetch_and_transform_jobs(remoteok_request, transform_remoteok_jobs, response_index=1),
        fetch_and_transform_jobs(findwork_request, lambda jobs: [create_job_entry(job) for job in jobs], result_key='results')
    )

    all_jobs = remotive_jobs + remoteok_jobs + findwork_jobs
    target_date = datetime.now().date() - timedelta(days=1)
    filtered_jobs = filter_jobs_by_date(all_jobs, target_date)

    jobs_df = pd.DataFrame(filtered_jobs)
    jobs_df = jobs_df[['title', 'company_name', 'url', 'job_type', 'location', 'salary_range', 'date']]
    return jobs_df

if __name__ == '__main__':
    jobs_df = asyncio.run(main())
    print(jobs_df)
