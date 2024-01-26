from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    # Маршрут к административной панели Django.
    path('admin/', admin.site.urls),

    # Маршрут к главной странице.
    path('', views.index, name='index'),

    # Маршрут к странице с загадками.
    path('riddle/', views.riddle, name='riddle'),

    # Маршрут к странице с ответами на загадки.
    path('answer/', views.answer, name='answer'),

    # Маршрут к странице умножения числа.
    path('multiply/', views.multiply, name='multiply'),

    # Маршрут к странице для генерации математических выражений.
    path('expression/', views.generate_expression, name='generate_expression'),

    # Маршрут к странице истории математических выражений.
    path('history/', views.expression_history, name='history'),

    # Маршрут к странице анализа введенной строки.
    path('str2words/', views.str2words_view, name='str2words'),

    # Маршрут к странице истории запросов анализа строк пользователя.
    path('str_history/', views.str_history, name='str_history'),

    # Маршрут к странице входа в систему.
    path('login/', views.LoginUser.as_view(), name='login'),

    # Маршрут для выхода из системы.
    path('logout/', views.logout_user, name='logout'),

    # Маршрут к странице регистрации нового пользователя.
    path('register/', views.RegisterUser.as_view(), name='register'),
]
