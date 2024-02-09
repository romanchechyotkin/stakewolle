import uuid


def generate_referral_code() -> str:
    return str(uuid.uuid4()).replace("-", "")[:12]