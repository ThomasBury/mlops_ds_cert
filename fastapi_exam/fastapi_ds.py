from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import datetime

responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}


api = FastAPI()
data = [1, 2, 3, 4, 5]

class MyException(Exception):
    def __init__(self,                 
                 name : str,
                 date: str):
        self.name = name
        self.date = date
        
@api.exception_handler(MyException)

def MyExceptionHandler(
    request: Request,
    exception: MyException
    ):
    return JSONResponse(
        status_code=418,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own', 
            'date': exception.date
        }
    )
    
@api.get('/my_custom_exception')
def get_my_custom_exception():
    raise MyException(
      name='my error',
      date=str(datetime.datetime.now())
      )
    
@api.get('/thing', responses=responses)
def get_thing():
    return {
        'data': 'hello world'
    }