# users/management/commands/load_test_data.py
from django.core.management.base import BaseCommand
from users.models import User
from access_controle.models import Role, BusinessElement, AccessRoleRule, UserRole

class Command(BaseCommand):
    help = 'Load test data into the database'

    def handle(self, *args, **options):
        self.stdout.write('Loading test data...')

        # Создаем роли
        admin_role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Full system access'}
        )
        user_role, _ = Role.objects.get_or_create(
            name='user',
            defaults={'description': 'Regular user'}
        )

        # Создаем бизнес-элементы (обязательно указываем resource_name!)
        products, _ = BusinessElement.objects.get_or_create(
            name='Products',
            defaults={
                'description': 'Product management',
                'resource_name': 'products'   # <-- добавлено
            }
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

        # Создаем пользователей (с учетом кастомной модели)
        admin, _ = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'is_superuser': True,
                'is_staff': True,      # важно для входа в админку
                'is_active': True,
            }
        )
        admin.set_password('admin1234')
        admin.save()

        user, _ = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'first_name': 'Regular',
                'last_name': 'User',
                'is_active': True,
            }
        )
        user.set_password('user1234')
        user.save()

        # Назначаем роль
        UserRole.objects.get_or_create(user=user, role=user_role)

        self.stdout.write(self.style.SUCCESS('Test data loaded successfully!'))
        self.stdout.write('Users:')
        self.stdout.write('  admin@example.com / admin1234')
        self.stdout.write('  user@example.com / user1234')