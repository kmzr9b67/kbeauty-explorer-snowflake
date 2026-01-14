import streamlit as st

from snowflake.sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, create_engine
from k_beauty_app.models import Products, AgeRanges, SkinType, Concerns


class DataBase:
    """Handles connection and operations with the Snowflake database.

    This class provides an interface to fetch product recommendations and 
    configuration keys for the Streamlit UI using SQLAlchemy ORM.

    Attributes:
        engine: SQLAlchemy engine connected to Snowflake.
        SessionLocal: Session factory for creating new database sessions.
    """
    def __init__(self) -> None:
        engine = create_engine(URL(
            account = st.secrets["snowflake"]["account"],
            user = st.secrets["snowflake"]["user"],
            password = st.secrets["snowflake"]["password"],
            role = st.secrets["snowflake"]["role"],
            warehouse = st.secrets["snowflake"]["warehouse"],
            database = st.secrets["snowflake"]["database"],
            schema = st.secrets["snowflake"]["schema"]
            ))
        self.session = sessionmaker(bind=engine)()


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
                .order_by(Products.step_id, Products.rating.desc()).limit(1)
            )
        results = session.execute(stmt).scalars().all()
        return [
            {
                "step": p.step_id,
                "brand": p.brand,
                "product_name": p.name,
                "rating": p.rating,
                "url": p.image_url,
            } for p in results
        ]

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
    
    @staticmethod
    @st.cache_resource
    def get_instance():
        """Static method to provide a cached singleton instance of DataBase.
        
        This ensures only one connection pool is created for the entire app.
        """
        return DataBase()
