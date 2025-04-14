from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
#     TokenVerifyView,
# )

from users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserListView,
    UserDeleteView,
    ToggleAdminView,
    UserMeView,
    UserDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('all/', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('<int:user_id>/admin/', ToggleAdminView.as_view(), name='toggle-admin'),

    # JWT
    # path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
