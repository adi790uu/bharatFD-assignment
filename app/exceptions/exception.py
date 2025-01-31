class CustomException(Exception):
    def __init__(self, name: str, message: str, status_code: int):
        self.status_code = status_code
        self.name = name
        self.message = message
