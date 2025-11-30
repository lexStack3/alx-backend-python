from django.conf import settings
from django.core.exceptions import PermissionDenied
from datetime import datetime, time
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


class RestrictAccessByTimeMiddleware:
    """
    Restricts access to the chat app during a timeframe.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_start = time(18, 0)
        self.allowed_end = time(21, 0)

    def __call__(self, request):
        current_time = datetime.now().time()
        accept = request.headers.get("Accept", "")

        if request.path.startswith("/conversations/"):
            if not (self.allowed_start <= current_time <= self.allowed_end):
                raise PermissionDenied(
                    "Access to the server is restricted during this time."
                )

        return self.get_response(request)
