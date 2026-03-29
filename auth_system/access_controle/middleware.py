from users.services import AuthService
from django.contrib.auth.models import AnonymousUser

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем токен из заголовка или куки
        token = request.headers.get('Authorization', '')
        if token.startswith('Bearer '):
            token = token[7:]
            print("huuuuuuuuuuuuuu")
        else:
            token = request.COOKIES.get('auth_token')

        if token:
            user = AuthService.get_user_from_token(token)
            request.user = user
        else:
            request.user =  AnonymousUser()

        response = self.get_response(request)
        print(response)
        return response