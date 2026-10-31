"""SQLite database operations using SQLAlchemy."""
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities.ideal_functions import IdealFunctions
from entities.schema import Base
from entities.training_data import TrainingData


class DatabaseManager:
    """Handles SQLite database operations using SQLAlchemy."""

    def __init__(self, db_path):
        """Create the engine and session factory for the given database file."""
        self.db_url = f"sqlite:///{db_path}"
        self.engine = create_engine(self.db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables (drops old ones if they exist)."""
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def insert_dataframe(self, df, table_name):
        """Insert a pandas DataFrame into a specific SQL table."""
        df.to_sql(table_name, con=self.engine, if_exists='append', index=False)

    def load_table_as_df(self, table_name):
        """Load an SQL table into a pandas DataFrame."""
        df = pd.read_sql_table(table_name, con=self.engine)
        return df