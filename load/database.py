from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from typing import Optional
import pandas as pd
from sqlalchemy.exc import OperationalError

class PostgresConnection:
    """
    A class to manage PostgreSQL database connection using SQLAlchemy.

    Attributes:
        url (str): The database URL constructed from environment variables.
        engine (Optional[Engine]): The SQLAlchemy engine connected to the database.
    """

    def __init__(self,db_user:str,db_password:str,db_host:str,db_database:str,db_port:str) -> None:
        """
        Initializes the PostgresConnection with the database URL.

        The database URL is constructed using environment variables: DB_USER, DB_PASSWORD, DB_HOST, and DB_DATABASE.
        """
        self.url: str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
        self.engine: Optional[Engine] = None

    def get_engine(self) -> Engine:
        """
        Creates and returns a SQLAlchemy engine for the PostgreSQL database.

        Returns:
            Engine: The SQLAlchemy engine connected to the PostgreSQL database.
        """
        self.engine = create_engine(self.url, poolclass=StaticPool)
        return self.engine

class DatabaseHandler:
    """
    A class for handling database operations, specifically loading data from a DataFrame 
    and removing outdated rows.

    Attributes:
        df (pd.DataFrame): The DataFrame containing data to be loaded into the database.
        table_name (str): The name of the database table to interact with.
        engine: The SQLAlchemy engine used to connect to the database.
    """

    def __init__(self, df: pd.DataFrame, table_name: str, engine):
        """
        Initializes the DatabaseHandler instance with a DataFrame, table name, and database engine.

        Args:
            df (pd.DataFrame): DataFrame containing data to be stored in the database.
            table_name (str): Name of the target database table.
            engine: SQLAlchemy engine for database connections.
        """
        self.df = df
        self.table_name = table_name
        self.engine = engine

    def load_to_database(self):
        """
        Loads the DataFrame into the specified database table.

        If the table already contains data, the method appends the new data to the existing records.

        Returns:
            None
        """
        self.df.to_sql(name=self.table_name, con=self.engine, if_exists='append', index=False)