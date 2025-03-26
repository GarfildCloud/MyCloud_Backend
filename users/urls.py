from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import RegisterView, LogoutView, UserListView, UserDeleteView, ToggleAdminView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('all/', UserListView.as_view(), name='user-list'),
    path('<int:user_id>/', UserDeleteView.as_view(), name='user-delete'),

    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('<int:user_id>/admin/', ToggleAdminView.as_view(), name='toggle-admin'),

]
