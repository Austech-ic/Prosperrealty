# exception_handler.py

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        if 'user_inactive' in str(response.data.get('code', '')):
            res = {
                "status": "Failed",
                "data": None,
                "message": "ACCOUNT HAS BEEN DELETED"
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        
    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        if 'No active account found with the given credentials' in str(response.data.get('detail', '')):
            res = {
                "status": "Failed",
                "data": None,
                "message": "ACCOUNT NOT FOUND,PLEASE CHECK YOUR EMAIL AND PASSWORD"
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        
    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        if 'user_not_found' in str(response.data.get('code', '')):
            res = {
                "status": "Failed",
                "data": None,
                "message": "INVALID TOKEN OR TOKEN EXPIRED,PLEASE LOGIN AGAIN"
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        
    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        if 'Authentication credentials were not provided' in str(response.data.get('detail', '')):
            res = {
                "status": "Failed",
                "data": None,
                "message": "AUTHENTICATION CREDENTIALS WERE NOT PROVIDED"
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        
    if response is not None and response.status_code == status.HTTP_403_FORBIDDEN:
        if 'Authentication credentials were not provided' in str(response.data.get('detail', '')):
            res = {
                "status": "Failed",
                "data": None,
                "message": "AUTHENTICATION CREDENTIALS WERE NOT PROVIDED"
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        
    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        if "token_not_valid" in str(response.data.get('code', '')):
            res = {
                "status": "Failed",
                "data": None,
                "message": "TOKEN IS EXPIRED OR INVALID,PLEASE LOGIN AGAIN"
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        
    if response is not None and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            res = {
                "status": "Failed",
                "data": None,
                "message": "INTERNAL_SERVER_ERROR"
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
