from django.urls import path
from user.views import LoginView, RegisterView, LogoutView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
