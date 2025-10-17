import uuid
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from src.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, UUID, DateTime
from src.utils import get_secret

def get_rds_uri() -> str:
    try:
        rds_uri = get_secret('RdsUri')
        return rds_uri
    except Exception as e:
        print(f'Failed to fetch RdsUri from secrets manager: {e}')
        raise e

rds_uri = get_rds_uri()
engine = create_engine(rds_uri)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()


class BlockedEmail(Base):
    __tablename__ = "blocked_emails"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False)
    app_uuid = Column(UUID, nullable=False)
    blocked_reason = Column(String(255), nullable=True)  # Optional field
    request_ip = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
