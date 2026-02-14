from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://postgres:mohana123@postgres:5432/puneeth"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

