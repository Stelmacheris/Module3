import dotenv
from extract.api_request import ApiRequest
import json
from datetime import datetime, timedelta

def transform_remotive_data(jobs):
    """Transform Remotive job data keys and date format."""
    for job in jobs:
        job['location'] = job.pop('candidate_required_location', '')
        job['date'] = job.pop('publication_date', '')
    return jobs

def transform_remoteok_data(jobs):
    """Transform RemoteOK job data keys and add additional fields."""
    for job in jobs:
        job['position'] = job.pop('title', '')
        job['company_name'] = job.pop('company', '')
        job['job_type'] = 'Remote'

        salary_min = job.get('salary_min', '')
        salary_max = job.get('salary_max', '')
        job['salary_range'] = f"{salary_min} - {salary_max}" if salary_min and salary_max else ''
    return jobs

def filter_jobs_by_yesterday(jobs):
    """Filter jobs created yesterday based on the date field."""
    yesterday = datetime.now().date() - timedelta(days=1)
    filtered_jobs = []
    for job in jobs:
        job_date_str = job.get('date', '')
        try:
            job_date = datetime.fromisoformat(job_date_str).date()
            if job_date == yesterday:
                filtered_jobs.append(job)
        except ValueError:
            continue
    return filtered_jobs

if __name__ == '__main__':
    api_request_1 = ApiRequest('https://remotive.com/api/remote-jobs?limit=50')
    response_text_1 = api_request_1.make_request()
    jobs_array_1 = []
    if response_text_1:
        json_data_1 = json.loads(response_text_1)
        jobs_array_1 = json_data_1.get('jobs', [])
        jobs_array_1 = transform_remotive_data(jobs_array_1)
    
    api_request_2 = ApiRequest('https://remoteok.com/api')
    response_text_2 = api_request_2.make_request()
    jobs_array_2 = []
    if response_text_2:
        json_data_2 = json.loads(response_text_2)
        jobs_array_2 = json_data_2[1:]  # Skip the first element
        jobs_array_2 = transform_remoteok_data(jobs_array_2)

    combined_jobs = jobs_array_1 + jobs_array_2
    
    yesterday_jobs = filter_jobs_by_yesterday(combined_jobs)

    with open('jobs_data.json', 'w') as f:
        json.dump(yesterday_jobs, f, indent=4)
