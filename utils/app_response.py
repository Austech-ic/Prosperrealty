from rest_framework.response import Response
from rest_framework import status

def app_response(success: bool, message: str, data=None, http_status=status.HTTP_200_OK,meta_data=None):
    """
    Utility function to create a generic response structure.
    """
    response = {
        "status": "success" if success else "failed",
        "message": message,
        "meta_data":meta_data,
        "data": data,
    }
    return Response(response, status=http_status)