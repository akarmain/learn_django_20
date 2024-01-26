from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('riddle/', views.riddle, name='riddle'),
    path('answer/', views.answer, name='answer'),
    path('multiply/', views.multiply, name='multiply'),
    path('expression/', views.generate_expression, name='generate_expression'),
    path('history/', views.expression_history, name='history'),
    path('str2words/', views.str2words_view, name='str2words'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
]



