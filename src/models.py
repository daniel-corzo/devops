import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BlockedEmail(db.Model):
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), nullable=False)
    app_uuid = db.Column(db.UUID, nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=False)
    request_ip = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
