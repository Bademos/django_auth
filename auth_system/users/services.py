from .models import User, Session
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

class AuthService:
    @staticmethod
    def login(email, password):
        try:
            user = User.objects.get(email=email, is_active=True)
            if user.check_password(password):
                token = user.generate_token()
                session = Session.objects.create(
                    user=user,
                    token=token,
                    expires_at=timezone.now() + timedelta(hours=24)
                )
                return token, user
        except User.DoesNotExist:
            pass
        return None, None

    @staticmethod
    def logout(token):
        try:
            session = Session.objects.get(token=token, is_active=True)
            print(session)
            session.is_active = False

            session.save()
            return True
        except Session.DoesNotExist:
            print("nam hana")
            return False

    @staticmethod
    def get_user_from_token(token):
        try:
            session = Session.objects.get(token=token, is_active=True)
            if timezone.now() < session.expires_at:
                return session.user
            else:
                session.is_active = False
                session.save()
        except Session.DoesNotExist:
            pass
        return None