from load.database import PostgresConnection,DatabaseHandler
import os
import dotenv
from transformation import create_statistic,clean_df

dotenv.load_dotenv(dotenv.find_dotenv('.env'))

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


if __name__ == '__main__':
    pc = PostgresConnection(DB_USER,DB_PASSWORD,DB_HOST,DB_DATABASE,DB_PORT)
    engine = pc.get_engine()

    job_listings_df = clean_df()
    statistics_df = create_statistic()

    print(statistics_df)

    db_handler_jobs = DatabaseHandler(job_listings_df,'job_listings',engine)
    db_handler_jobs.load_to_database()

    db_handler_statsitics = DatabaseHandler(statistics_df,'job_statistics',engine)
    db_handler_statsitics.load_to_database()





    