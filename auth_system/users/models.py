from django.db import models
from django.db import models
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings

class User(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, password):
        """Хеширование пароля с помощью bcrypt"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Проверка пароля"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def generate_token(self):
        """Генерация JWT токена"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    @property
    def is_authenticated(self):
        """
        Всегда возвращает True для аутентифицированных пользователей.
        Это свойство требуется Django и DRF.
        """
        return True

    @property
    def is_anonymous(self):
        """
        Всегда возвращает False для аутентифицированных пользователей.
        """
        return False

    def has_perm(self, perm, obj=None):
        """
        Проверка прав доступа (упрощенная версия).
        Можете расширить для интеграции с вашей RBAC системой.
        """
        if self.is_superuser:
            return True
        # Здесь можно добавить проверку через вашу RBAC систему
        return False

    def has_module_perms(self, app_label):
        """
        Проверка прав на модуль.
        """
        if self.is_superuser:
            return True
        return False

    class Meta:
        db_table = 'users'

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sessions'
# Create your models here.
