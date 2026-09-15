# It will handle:

# Defining the common foundation for all SQLAlchemy models
# Mapping Python models to database tables

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass