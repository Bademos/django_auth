# 🔐 RBAC система управления доступом

**Role-Based Access Control** система на Django с JWT аутентификацией

---

## 📖 О проекте

Проект представляет собой реализацию RBAC (Role-Based Access Control) системы для управления доступом к ресурсам. Разработан на Django REST Framework с использованием JWT токенов для аутентификации.

### Основные возможности
- JWT аутентификация с хранением токенов в HttpOnly cookies
- Множественные роли у одного пользователя
- Бизнес-элементы — гибкое определение ресурсов
- Детальные права (CRUD с разделением на "свои" и "все" объекты)
- Суперпользователь с полным доступом
- Готовая API структура

---

## 🏗️ Структура проекта
```
auth_system/
├── users/                              # Модуль управления пользователями
│   ├── models.py                       # User, Session модели
│   ├── services.py                     # AuthService (JWT, логика аутентификации)
│   ├── serializers.py                  # Валидация данных
│   ├── views.py                        # API endpoints
│   └── utils.py                        # Вспомогательные функции
│
├── access_control/                     # Ядро RBAC системы (исправлено название)
│   ├── models.py                       # Role, BusinessElement, AccessRoleRule, UserRole
│   ├── permissions.py                  # AccessChecker (логика проверки прав)
│   ├── middleware.py                   # AuthMiddleware (извлечение пользователя)
│   ├── serializers.py                  # Сериализаторы для RBAC моделей
│   ├── views.py                        # API для управления ролями и правами
│   └── exceptions.py                   # Кастомные исключения RBAC
│
├── mock_business/                      # Тестовый бизнес-модуль
│   ├── models.py                       # Пример бизнес-моделей
│   ├── views.py                        # Пример использования RBAC
│   ├── serializers.py                  # Сериализаторы для бизнес-моделей
│   └── permissions.py                  # Бизнес-специфичные проверки
│
└── auth_system/                        # Основные настройки
    ├── settings.py                     # Django настройки
    ├── urls.py                         # Главный URLConf
    ├── wsgi.py                         # WSGI конфигурация
    ├── asgi.py                         # ASGI конфигурация
    └── celery.py                       # Celery конфигурация (опционально)s.py
└── urls.py
```

---

## 🔐 Модель прав доступа

Каждое правило связывает **роль** с **бизнес-элементом** и определяет 7 уровней доступа:

| Право | Описание | Применение |
|-------|----------|------------|
| `read_permission` | Чтение своих объектов | `owner_id == user.id` |
| `read_all_permission` | Чтение всех объектов | Любые объекты |
| `create_permission` | Создание объектов | Новые записи |
| `update_permission` | Редактирование своих объектов | `owner_id == user.id` |
| `update_all_permission` | Редактирование всех объектов | Любые объекты |
| `delete_permission` | Удаление своих объектов | `owner_id == user.id` |
| `delete_all_permission` | Удаление всех объектов | Любые объекты |

## 📂 Структура базы данных

### Таблица `users`
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | BIGINT | Первичный ключ |
| `email` | VARCHAR(254) | Уникальный email пользователя |
| `password_hash` | VARCHAR(128) | Хеш пароля (bcrypt) |
| `first_name` | VARCHAR(50) | Имя |
| `last_name` | VARCHAR(50) | Фамилия |
| `middle_name` | VARCHAR(50) | Отчество (опционально) |
| `is_active` | BOOLEAN | Активен ли пользователь |
| `is_superuser` | BOOLEAN | Суперпользователь |
| `created_at` | TIMESTAMP | Дата создания |
| `updated_at` | TIMESTAMP | Дата обновления |

---

### Таблица `sessions`
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | BIGINT | Первичный ключ |
| `user_id` | BIGINT | FK на `users.id` |
| `token` | VARCHAR(500) | JWT токен (уникальный) |
| `expires_at` | TIMESTAMP | Дата истечения токена |
| `is_active` | BOOLEAN | Активна ли сессия |

---

### Таблица `roles`
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | BIGINT | Первичный ключ |
| `name` | VARCHAR(50) | Название роли (уникальное) |
| `description` | TEXT | Описание роли |
| `created_at` | TIMESTAMP | Дата создания |

---

### Таблица `business_elements`
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | BIGINT | Первичный ключ |
| `name` | VARCHAR(100) | Название элемента (уникальное) |
| `resource_name` | VARCHAR(100) | Имя ресурса для проверки прав |
| `description` | TEXT | Описание элемента |

---

### Таблица `access_roles_rules`
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | BIGINT | Первичный ключ |
| `role_id` | BIGINT | FK на `roles.id` |
| `element_id` | BIGINT | FK на `business_elements.id` |
| `read_permission` | BOOLEAN | Чтение своих объектов |
| `read_all_permission` | BOOLEAN | Чтение всех объектов |
| `create_permission` | BOOLEAN | Создание объектов |
| `update_permission` | BOOLEAN | Обновление своих объектов |
| `update_all_permission` | BOOLEAN | Обновление всех объектов |
| `delete_permission` | BOOLEAN | Удаление своих объектов |
| `delete_all_permission` | BOOLEAN | Удаление всех объектов |

---

### Таблица `user_roles`
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | BIGINT | Первичный ключ |
| `user_id` | BIGINT | FK на `users.id` |
| `role_id` | BIGINT | FK на `roles.id` |
| `assigned_at` | TIMESTAMP | Дата назначения роли |

---

### Связи между таблицами


### Алгоритм проверки прав

```python
def check_permission(user, resource_name, action, obj=None):
    # 1. Проверка активности пользователя
    if not user or not user.is_active:
        return False
    
    # 2. Суперпользователь имеет все права
    if user.is_superuser:
        return True
    
    # 3. Получение ролей пользователя
    user_roles = UserRole.objects.filter(user=user)
    
    # 4. Поиск бизнес-элемента
    element = BusinessElement.objects.get(resource_name=resource_name)
    
    # 5. Получение правил для ролей
    rules = AccessRoleRule.objects.filter(
        role_id__in=user_roles.values_list('role_id'),
        element=element
    )
    
    # 6. Проверка прав с учетом владельца
    for rule in rules:
        if action == 'read':
            if obj and obj.owner_id == user.id and rule.read_permission:
                return True
            if rule.read_all_permission:
                return True
        # ... аналогично для update, delete
    return False