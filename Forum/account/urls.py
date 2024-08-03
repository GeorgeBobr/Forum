from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from account.views import RegistrationView, ProfileView, UserChangeView, UserPasswordChangeView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name="register/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('<int:pk>/profile/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/profile/edit/', UserChangeView.as_view(), name='profile_change'),
    path('<int:pk>/profile/password-change/', UserPasswordChangeView.as_view(), name='password_change'),
]
