from src.logger import logging
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = self.error_message_detail(error_message, error_detail)

    def error_message_detail(self, error, error_detail):
        _, _, exc_tb = error_detail  # Unpack the traceback from exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        error_message = "Error in script [{0}] line [{1}] error message [{2}]".format(
            file_name, exc_tb.tb_lineno, str(error)
        )
        return error_message

    def __str__(self):
        return self.error_message


if __name__=="__main__":

    try:
        a=1/0
    except Exception as e:
        logging.info("logging started")
        raise CustomException(e,sys)
