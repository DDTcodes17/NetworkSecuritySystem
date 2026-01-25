import sys

def error_message_details(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured in python script {filename} line number {exc_tb.tb_lineno} error message {error}"
    return error_message

class NetworkSecurityException(Exception):
    def __init__(self,error, error_detail:sys):
        super().__init__(error)
        self.error = error_message_details(error=error, error_detail=error_detail)

    def __str__(self):
        return self.error

if __name__ == "__main__":
    try:
        a=1/0
        print("This will not print")
    except Exception as e:
        raise NetworkSecurityException(e,sys)        