import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Load test data into the database if empty'

    def handle(self, *args, **options):
        self.stdout.write('Checking if database needs test data...')

        # Проверяем, пуста ли база данных
        if User.objects.exists():
            self.stdout.write(self.style.WARNING('Database already has users. Skipping test data load.'))
            return

        self.stdout.write('Database is empty. Loading test data...')

        try:
            # Импортируем модели внутри функции, чтобы избежать проблем с импортом
            from access_control.models import Role, BusinessElement, AccessRoleRule, UserRole

            # Создаем роли
            admin_role, _ = Role.objects.get_or_create(
                name='admin',
                defaults={'description': 'Full system access'}
            )
            user_role, _ = Role.objects.get_or_create(
                name='user',
                defaults={'description': 'Regular user'}
            )

            # Создаем бизнес-элементы
            products, _ = BusinessElement.objects.get_or_create(
                name='Products',
                defaults={'description': 'Product management', 'resource_name': 'products'}
            )

            # Создаем правила для админа
            AccessRoleRule.objects.get_or_create(
                role=admin_role,
                element=products,
                defaults={
                    'read_permission': True,
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_permission': True,
                    'update_all_permission': True,
                    'delete_permission': True,
                    'delete_all_permission': True
                }
            )

            # Создаем правила для обычного пользователя
            AccessRoleRule.objects.get_or_create(
                role=user_role,
                element=products,
                defaults={
                    'read_permission': True,
                    'read_all_permission': False,
                    'create_permission': True,
                    'update_permission': True,
                    'update_all_permission': False,
                    'delete_permission': True,
                    'delete_all_permission': False
                }
            )

            # Создаем тестовых пользователей
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin1234',
                first_name='Admin',
                last_name='User',
                is_active=True
            )

            user = User.objects.create_user(
                username='user',
                email='user@example.com',
                password='user1234',
                first_name='Regular',
                last_name='User',
                is_active=True
            )

            # Назначаем роли
            UserRole.objects.get_or_create(user=user, role=user_role)

            self.stdout.write(self.style.SUCCESS('✓ Test data loaded successfully!'))
            self.stdout.write('Users created:')
            self.stdout.write('  admin@example.com / admin1234 (admin)')
            self.stdout.write('  user@example.com / user1234 (regular user)')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading test data: {e}'))
            raise