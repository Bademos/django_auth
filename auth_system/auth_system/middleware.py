# auth_system/middleware.py
from django.utils.deprecation import MiddlewareMixin

class ForceDisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Принудительно отключаем CSRF проверку для всех API запросов
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
            print(f"CSRF disabled for: {request.path}")