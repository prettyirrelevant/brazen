from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


def success_response(data, status_code=HTTP_200_OK):
    """Generate a success response with the provided data and status code."""
    return Response({'data': data}, status=status_code)


def error_response(message, errors, status_code=HTTP_400_BAD_REQUEST):
    """Generate an error response with the provided message, errors, and status code."""
    error_data = {'errors': errors, 'message': message}
    return Response(error_data, status=status_code)
