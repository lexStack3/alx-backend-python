from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseForbidden
from datetime import datetime, time, timedelta
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


class OffensiveLanguageMiddleware:
    """
    Limits the number of chat messages a user can send within a certain time
    window, based on their IP address.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.time_window = timedelta(minutes=1)
        self.max_requests = 5
        self.ip_request_log = {}

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            if ip not in self.ip_request_log:
                self.ip_request_log[ip] = []

            timestamps = [
                t for t in self.ip_request_log[ip]
                if now - t < self.time_window
            ]

            if len(timestamps) >= self.max_requests:
                accept = request.headers.get("Accept", "")
                if "application/json" in accept:
                    return JsonResponse(
                        {"error": "Rate limit exceeded. Try again later."},
                        status=429
                    )
                return HttpResponseForbidden(
                    "<h3>429 Too Many Requests</h3><p>Please wait a minute.</p>"
                )

            timestamps.append(now)
            self.ip_request_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Returns a user's IP address
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get("REMOTE_ADDR")
