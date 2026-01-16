from functools import wraps

def validate_db_tables(func):
    """Decorator to ensure database tables exist before executing a database operation.

    This decorator acts as a safety layer for database queries. If a query fails 
    because a table or object is missing (common in fresh Snowflake environments), 
    it catches the specific exception, triggers the database population scripts, 
    and retries the original function call.

    Logic Flow:
        1. Attempts to execute the decorated function.
        2. If a 'ProgrammingError' occurs, it checks the error message for 
           keywords like 'does not exist' or 'invalid identifier'.
        3. If found, it calls 'self.populate_database()' to rebuild the schema.
        4. On successful population, it re-executes the original function.
        5. If the error is unrelated or population fails, it re-raises the exception.

    Args:
        func (callable): The database-dependent method to be decorated (e.g., get_keys).

    Returns:
        callable: The wrapped function that includes error handling and auto-initialization.

    Raises:
        Exception: Re-raises the original exception if it is not related to missing 
                  database objects or if the initialization process fails.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            error_msg = str(e).lower()
            if "does not exist" in error_msg or "invalid identifier" in error_msg:
                if self.populate_database():
                    return func(self, *args, **kwargs)
            else:
                raise e
    return wrapper