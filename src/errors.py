from src import logger

class ErrorType:
    S3 = "S3 Error"

class CustomError500(Exception):
    def __init__(self, msg="", error_type: str = ""):
        self.status_code = 500
        self.detail = f"{error_type}. {msg}"

def error_500(msg="", error_type: str = ""):
    full_message = f"HTTP: 500 - {error_type}. {msg}"
    logger.error(full_message)
    # rollbar_logger.rollbar_message(full_message, level="error")
    raise CustomError500(msg, error_type)

