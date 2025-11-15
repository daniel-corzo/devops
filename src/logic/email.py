from src.models import session, BlockedEmail
import uuid


def run_block_email_validations(email: str, app_uuid: str, blocked_reason: str = None):
    if not email or (isinstance(email, str) and not email.strip()):
        return {"message": "Email is required"}

    if not app_uuid or (isinstance(app_uuid, str) and not app_uuid.strip()):
        return {"message": "App UUID is required"}

    try:
        uuid.UUID(app_uuid)
    except ValueError:
        return {"message": "Invalid app UUID format"}

    if session.query(BlockedEmail).filter_by(email=email).first():
        return {"message": "Email already blocked"}
