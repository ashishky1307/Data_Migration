from sqlalchemy import (
    create_engine,
    Column,
    DateTime,
    Float,
    String,
    text
)
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

engine = create_engine(DB_URL)

Base = declarative_base()


class Metric(Base):
    __tablename__ = "metrics"

    time = Column(DateTime(timezone=True), primary_key=True)
    tag_id = Column(String, primary_key=True)
    metric_name = Column(String)
    value = Column(Float)


if __name__ == "__main__":

    # Create PostgreSQL table
    Base.metadata.create_all(engine)
    
    # Convert to TimescaleDB hypertable
    with engine.connect() as conn:
        conn.execute(text("""
            SELECT create_hypertable(
                'metrics',
                'time',
                if_not_exists => TRUE
            );
        """))
        conn.commit()

    print("hypertable created successfully")