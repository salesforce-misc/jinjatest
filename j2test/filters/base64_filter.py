import base64


def base64_encode(data: str) -> str:
    return base64.b64encode(data.encode()).decode()


def base64_decode(encoded: str) -> str:
    return base64.b64decode(encoded).decode()
