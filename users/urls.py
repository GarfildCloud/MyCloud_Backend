from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from users.views import custom_logout

def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

from users.views import (
    RegisterView,
    LoginView,
    UserListView,
    ToggleAdminView,
    UserMeView,
    UserDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('csrf/', ensure_csrf_cookie(get_csrf_token), name='csrf'),
    
    path('all/', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('<int:user_id>/admin/', ToggleAdminView.as_view(), name='toggle-admin'),
]
