FROM apache/airflow:2.10.2-python3.8

#COPY ./ ./

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

USER airflow