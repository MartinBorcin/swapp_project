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
    path('logout/', views.user_logout, name='logout'),
    path('select-checkout/', views.select_checkout, name='select-checkout'),
    path('new-checkout/', views.new_checkout, name='new-checkout'),
    path('checkout/<checkout_id>/', views.checkout, name='checkout'),
    path('checkout/<checkout_id>/export/', views.checkout_export, name='checkout-export'),
    path('manage/refresh-status/', views.refresh_status, name='refresh-status'),
]
