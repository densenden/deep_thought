from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from sqlalchemy.exc import OperationalError
import time

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:bqs4?f7+*QLqvM*@db.xbrrlnaycpvygaqzeceg.supabase.co:5432/postgres")

# Verbindungsoptionen für bessere Stabilität
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class QARecord(Base):
    __tablename__ = "qa_records"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("Datenbanktabellen erfolgreich erstellt!")
            return
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Verbindungsversuch {attempt + 1} fehlgeschlagen. Versuche erneut in {retry_delay} Sekunden...")
                time.sleep(retry_delay)
            else:
                print("Konnte keine Verbindung zur Datenbank herstellen.")
                raise e

# Initialisiere die Datenbank
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 