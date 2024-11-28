import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        """
        Initialize the NetworkSecurityException.

        Args:
            error_message (str): A brief description of the error.
            error_details (sys): The sys module object containing error information.

        Attributes:
            error_message (str): A brief description of the error.
            error_details (sys): The sys module object containing error information.
        """
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        """
        Return a string representation of the exception.

        Returns:
            str: A formatted string containing the error message, line number, and filename.
        """
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.filename, 
            self.lineno, 
            str(self.error_message)
            )

if __name__ == "__main__":
    try:
        logger.logging.info("Enter the try block")
        a = 1/0
        print('This will not be printed.')
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
