from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import (
    RegisterView,
    LogoutView,
    UserListView,
    UserDeleteView,
    ToggleAdminView,
    CustomTokenObtainPairView, UserMeView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('all/', UserListView.as_view(), name='user-list'),
    path('<int:user_id>/', UserDeleteView.as_view(), name='user-delete'),
    path('me/', UserMeView.as_view(), name='user-me'),

    # JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('<int:user_id>/admin/', ToggleAdminView.as_view(), name='toggle-admin'),

]
