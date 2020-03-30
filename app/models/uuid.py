import uuid


def generate(prefix: str = "") -> str:
    return prefix + str(uuid.uuid4())
