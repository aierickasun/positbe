from django.urls import path,include
from users import views

urlpatterns = [
    path('users-login/',views.UserLogin.as_view()),
    path('users-registration/',views.UserRegistration.as_view())
]
