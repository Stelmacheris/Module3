#FROM apache/airflow:slim-2.10.2
FROM apache/airflow:2.10.2-python3.8

COPY ./ ./
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

USER airflow
EXPOSE 8080
EXPOSE 8793
EXPOSE 5555