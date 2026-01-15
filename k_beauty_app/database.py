import os 
import streamlit as st

from snowflake.sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, create_engine, text
from k_beauty_app.models import Products, AgeRanges, SkinType, Concerns
from k_beauty_app.validation import validate_db_tables

class DataBase:
    """Handles connection and operations with the Snowflake database.

    This class provides an interface to fetch product recommendations and 
    configuration keys for the Streamlit UI using SQLAlchemy ORM.

    Attributes:
        engine: SQLAlchemy engine connected to Snowflake.
        SessionLocal: Session factory for creating new database sessions.
    """
    def __init__(self) -> None:
        self.engine = create_engine(URL(
            account = st.secrets["snowflake"]["account"],
            user = st.secrets["snowflake"]["user"],
            password = st.secrets["snowflake"]["password"],
            role = st.secrets["snowflake"]["role"],
            warehouse = st.secrets["snowflake"]["warehouse"],
            database = st.secrets["snowflake"]["database"],
            schema = st.secrets["snowflake"]["schema"]
            ))
        self.session = sessionmaker(bind=self.engine)()

    @validate_db_tables
    def get_recommendations(self, age_val: str, skin_val: str, concern_val: str):
        """Fetches a list of recommended products based on user criteria.

        Executes a SQL query performing JOINs across Products, AgeRanges, 
        SkinType, and Concerns tables.

        Args:
            age_val: The name of the age group (e.g., '20s').
            skin_val: The name of the skin type (e.g., 'Oily').
            concern_val: The name of the primary skin concern (e.g., 'Acne').

        Returns:
            A list of dictionaries where each dictionary contains product details:
            step, brand, product_name, rating, and image url.
        """
        with self.session as session:
            stmt = (
                select(Products)
                .join(AgeRanges, Products.age_range_id == AgeRanges.id)
                .join(SkinType, Products.skin_type_id == SkinType.id)
                .join(Concerns, Products.concern_id == Concerns.id)
                .where(
                    AgeRanges.name == age_val,
                    SkinType.name == skin_val,
                    Concerns.name == concern_val
                )
                .order_by(Products.step_id, Products.rating.desc()).limit(5)
            )
        results = session.execute(stmt).scalars().all()
        return [
            {
                "step": p.step_id,
                "brand": p.brand,
                "product_name": p.name,
                "rating": p.rating,
            } for p in results
        ]
    @validate_db_tables
    def get_keys(self, table_name):
        """Retrieves a list of unique names from a specific reference table.

        A generic method used to populate dropdown menus (selectboxes) 
        in the Streamlit user interface.

        Args:
            table_name: The ORM mapping class (e.g., SkinType, Concerns) 
                from which to fetch names.

        Returns:
            A list of unique strings from the 'name' column of the given table.
        """
        with self.session as session:
            stmt = (
                select(table_name.name).distinct()
            )
        return session.execute(stmt).scalars().all()
    
    def populate_database(self) -> bool:
        """Orchestrates the complete database initialization and seeding process.

        Sequentially executes a series of SQL scripts to set up the database schema, 
        populate reference tables (dictionaries), and generate the product 
        recommendation matrix. The order of execution is critical to maintain 
        referential integrity (Foreign Key constraints).

        Execution Order:
            1. 01_schema.sql: Creates tables and relationships.
            2. 02_dictionaries.sql: Inserts static data (Skin Types, Concerns, etc.).
            3. 03_products_data.sql: Generates the product mapping using logic.

        Returns:
            bool: True if all scripts were executed successfully in the correct order, 
                False if any script execution failed.
        """
        files = [
            'sql_scripts/01_schema.sql',
            'sql_scripts/02_dictionaries.sql',
            'sql_scripts/03_products_data.sql'
        ]
        
        for file in files:
            if not self.run_sql_file(file):
                return False
        return True

    def run_sql_file(self, file_path: str) -> bool:
        """Reads and executes a SQL file containing multiple commands.

        This method parses a file, splits its content by semicolons into individual 
        statements, and executes them sequentially within a single database connection. 
        It is primarily used for database schema initialization and data seeding.

        Args:
            file_path (str): The relative or absolute path to the .sql file to be executed.

        Returns:
            bool: True if all commands were executed successfully, False if the file 
                does not exist or a database error occurred during execution.
        """
        if not os.path.exists(file_path):
            return False
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            commands = [c.strip() for c in content.split(';') if c.strip()]
            
        try:
            with self.engine.connect() as conn:
                for command in commands:
                    conn.execute(text(command))
                conn.commit()
            return True
        except Exception as e:
            return False
    
    @staticmethod
    @st.cache_resource
    def get_instance():
        """Static method to provide a cached singleton instance of DataBase.
        
        This ensures only one connection pool is created for the entire app.
        """
        return DataBase()
