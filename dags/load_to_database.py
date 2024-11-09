from load.database import PostgresConnection,DatabaseHandler
import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def insert_to_database(**kwargs):
    pc = PostgresConnection(DB_USER,DB_PASSWORD,DB_HOST,DB_DATABASE,DB_PORT)
    engine = pc.get_engine()

    ti = kwargs['ti']
    job_listings_df,statistics_df = ti.xcom_pull(task_ids='create_statistic')

    db_handler_jobs = DatabaseHandler(job_listings_df,'job_listings',engine)
    db_handler_jobs.load_to_database()

    db_handler_statsitics = DatabaseHandler(statistics_df,'job_statistics',engine)
    db_handler_statsitics.load_to_database()





    