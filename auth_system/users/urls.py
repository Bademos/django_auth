from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, DeleteAccountView, UserListView, TestAuthView, GetCSRFTokenView
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', csrf_exempt(LogoutView.as_view()), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete/', DeleteAccountView.as_view(), name='delete'),
    path('test-auth/', TestAuthView.as_view(), name='test-auth'),
    path('get-csrf/', GetCSRFTokenView.as_view(), name='get-csrf'),

]