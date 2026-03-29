from .models import AccessRoleRule, UserRole


class AccessChecker:
    @staticmethod
    def check_permission(user, resource_name, action, obj=None):
        """
        Проверка прав доступа пользователя
        action: 'read', 'create', 'update', 'delete'
        """
        if not user or not user.is_active:
            return False

        # Суперпользователь имеет все права
        if user.is_superuser:
            return True

        # Получаем роли пользователя
        user_roles = UserRole.objects.filter(user=user)
        if not user_roles.exists():
            return False

        # Получаем бизнес-элемент
        try:
            from .models import BusinessElement
            element = BusinessElement.objects.get(resource_name=resource_name)
        except BusinessElement.DoesNotExist:
            return False

        # Получаем правила для ролей
        role_ids = [ur.role_id for ur in user_roles]
        rules = AccessRoleRule.objects.filter(
            role_id__in=role_ids,
            element=element
        )

        if not rules.exists():
            return False

        # Проверяем права
        for rule in rules:
            if action == 'read':
                if obj and hasattr(obj, 'owner_id') and obj.owner_id == user.id:
                    if rule.read_permission:
                        return True
                if rule.read_all_permission:
                    return True
            elif action == 'create':
                if rule.create_permission:
                    return True
            elif action == 'update':
                if obj and hasattr(obj, 'owner_id') and obj.owner_id == user.id:
                    if rule.update_permission:
                        return True
                if rule.update_all_permission:
                    return True
            elif action == 'delete':
                if obj and hasattr(obj, 'owner_id') and obj.owner_id == user.id:
                    if rule.delete_permission:
                        return True
                if rule.delete_all_permission:
                    return True

        return False