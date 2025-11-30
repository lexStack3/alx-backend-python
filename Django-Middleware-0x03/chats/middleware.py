from django.conf import settings
from datetime import datetime
import os


class RequestLoggingMiddleware:
    """
    Logs each user's requests to 'requests.log'
    Format: Date - User: {lex} - Path: /conversation/
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        log_path = os.path.join(settings.BASE_DIR, "requests.log")

        with open(log_path, 'a') as log_file:
            log_file.write(
                f"{datetime.now()} - User: {user} - Path: {request.path}\n"
            )

        return self.get_response(request)
