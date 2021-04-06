from django.urls import path
from .views import UserSignUpView, UserEditView, PasswordsChangeView
from . import views

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name="signup"),
    path('edit_profile/', UserEditView.as_view(), name="Edit-Profile"),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    path('password_updated/', views.password_success, name='password_success'),
]