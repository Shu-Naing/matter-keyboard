from django.db import models

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 400:
            self.save_error(request, response)
        return response

    def save_error(self, request, response):
        # Extract relevant information from the request and response
        url = request.path
        method = request.method
        status_code = response.status_code
        error_message = response.data.get('error') if hasattr(response, 'data') else None

        # Save the error to the database
        error = ErrorLog(url=url, method=method, status_code=status_code, error_message=error_message)
        error.save()
