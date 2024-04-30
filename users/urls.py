from django.urls import path
from users import views

app_name = 'users'  # Пространство имен для URL-адресов

urlpatterns = [
    # Вход пользователя
    path('login/', views.LoginView.as_view(), name='login'),
    # Регистрация нового пользователя
    path('registration/', views.RegistrationView.as_view(),
         name='registration'),
    # Профиль пользователя
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # Корзина пользователя
    path('users-cart/', views.UsersCartView.as_view(), name='users_cart'),
    # Выход пользователя
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
