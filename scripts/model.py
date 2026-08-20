from sqlalchemy import (
    create_engine,
    Column,
    DateTime,
    Float,
    String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

# PostgreSQL Configuration
POSTGRES = {
    "host": "localhost",
    "port": 5432,
    "database": "migration_db",
    "user": "postgres",
    "password": "postgres"
}

# Connection URL
DB_URL = (
    f"postgresql+psycopg2://"
    f"{POSTGRES['user']}:{POSTGRES['password']}@"
    f"{POSTGRES['host']}:{POSTGRES['port']}/"
    f"{POSTGRES['database']}"
)

# Database Engine
engine = create_engine(DB_URL)

# Base Class
Base = declarative_base()


class Metric(Base):

    __tablename__ = "metrics"

    time = Column(DateTime(timezone=True), primary_key=True)
    metric_name = Column(String, primary_key=True)
    value = Column(Float)
    tags = Column(JSONB)


# Create table
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Metrics table created successfully")