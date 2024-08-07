from rest_framework.response import Response
from rest_framework import status

class ResponseManager:
    '''properly handles responses'''

    def __init__(self, _type="error", message=None, data=None, status_code=400, **kwargs):
        '''initializes the response manager and return a response immediately'''
        self.handle_response(
            _type=_type,
            message=message,
            data=data,
            status_code=status_code
        )

    @staticmethod
    def handle_response(_type="error", message=None, data=None, status_code=400):
        '''dynamically sends a response'''
        return Response(
            {   "type": _type,
                "message": message,
                "data": data
            },
            status=status_code
        )
