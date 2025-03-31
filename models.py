from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from sqlalchemy.exc import OperationalError
import time
import logging
from contextlib import contextmanager

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:bqs4?f7+*QLqvM*@db.xbrrlnaycpvygaqzeceg.supabase.co:5432/postgres")

# Verbindungsoptionen für Serverless-Umgebungen
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,  # Reduziert auf 5 Minuten
    connect_args={
        "connect_timeout": 5,  # Reduziert auf 5 Sekunden
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    },
    pool_size=1,  # Minimale Pool-Größe für Serverless
    max_overflow=0,  # Keine zusätzlichen Verbindungen
    pool_timeout=30  # Timeout für Pool-Operationen
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
    max_retries = 2  # Reduzierte Anzahl von Versuchen
    retry_delay = 2  # Kürzere Wartezeit
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Versuche Datenbankverbindung herzustellen (Versuch {attempt + 1}/{max_retries})")
            Base.metadata.create_all(bind=engine)
            logger.info("Datenbanktabellen erfolgreich erstellt!")
            return
        except OperationalError as e:
            logger.error(f"Datenbankverbindungsfehler: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Warte {retry_delay} Sekunden vor erneutem Versuch...")
                time.sleep(retry_delay)
            else:
                logger.error("Konnte keine Verbindung zur Datenbank herstellen.")
                raise e
        except Exception as e:
            logger.error(f"Unerwarteter Fehler: {str(e)}")
            raise e

# Initialisiere die Datenbank
try:
    init_db()
except Exception as e:
    logger.error(f"Fehler bei der Datenbankinitialisierung: {str(e)}")
    # Erlaube der Anwendung trotzdem zu starten
    pass

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Fehler bei der Datenbankverbindung: {str(e)}")
        raise
    finally:
        db.close() 