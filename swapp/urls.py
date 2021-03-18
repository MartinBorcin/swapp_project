from django.urls import path
from swapp import views

app_name = 'swapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('items/', views.items, name='items'),
    path('about/', views.about, name='about'),
    path('sellers/', views.sellers, name='sellers'),
    path('my-items/', views.my_items, name='my-items'),
    path('manage/', views.manage, name='manage'),
    path('logout/', views.user_logout, name='logout')
]