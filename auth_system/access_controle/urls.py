from django.urls import path
from .views import RoleListView, AccessRuleListView

urlpatterns = [
    path('roles/', RoleListView.as_view(), name='roles'),
    path('rules/', AccessRuleListView.as_view(), name='rules'),
]