from functools import wraps
from sqlalchemy import text

def validate_db_tables(func):
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