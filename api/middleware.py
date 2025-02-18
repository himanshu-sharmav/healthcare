from django.http import JsonResponse
from rest_framework import status

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        return JsonResponse({
            'error': str(exception),
            'detail': 'An error occurred while processing your request.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 