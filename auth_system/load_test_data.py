import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_system.settings')
django.setup()

from users.models import User
from access_controle.models import Role,BusinessElement, AccessRoleRule, UserRole


def load_test_data():
    print("Загрузка тестовых данных...")

    # Создаем роли
    admin_role = Role.objects.create(name='admin', description='Full system access')
    user_role = Role.objects.create(name='user', description='Regular user')

    # Создаем бизнес-элементы
    products = BusinessElement.objects.create(
        name='Products',
        description='Product management'
    )

    # Создаем правила для админа
    AccessRoleRule.objects.create(
        role=admin_role,
        element=products,
        read_permission=True,
        read_all_permission=True,
        create_permission=True,
        update_permission=True,
        update_all_permission=True,
        delete_permission=True,
        delete_all_permission=True
    )

    # Создаем правила для обычного пользователя
    AccessRoleRule.objects.create(
        role=user_role,
        element=products,
        read_permission=True,
        read_all_permission=False,
        create_permission=True,
        update_permission=True,
        update_all_permission=False,
        delete_permission=True,
        delete_all_permission=False
    )

    # Создаем тестовых пользователей
    admin = User.objects.create(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        is_superuser=True,
        is_active=True
    )
    admin.set_password('admin1234')
    admin.save()

    user = User.objects.create(
        email='user@example.com',
        first_name='Regular',
        last_name='User',
        is_active=True
    )
    user.set_password('user1234')
    user.save()

    # Назначаем роли
    UserRole.objects.create(user=user, role=user_role)

    print("Тестовые данные загружены!")
    print("Пользователи:")
    print("  admin@example.com / admin1234")
    print("  user@example.com / user1234")


if __name__ == "__main__":
    load_test_data()