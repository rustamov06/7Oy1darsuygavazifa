from django.urls import path
from .views import (
    CarsListView, ColorDetailView, BrandDetailView, CarDetailView,
    UserRegisterView, UserLoginView, UserLogoutView, ProfileDetailView,
    SendEmailView, AddBrandView, AddCarView, AddColorView
)

urlpatterns = [
    path('', CarsListView.as_view(), name='index'),
    path('color/<int:pk>/', ColorDetailView.as_view(), name='color_detail'),
    path('brand/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),

    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile'),

    path('send_message/', SendEmailView.as_view(), name='send_message'),

    path('add_brand/', AddBrandView.as_view(), name='add_brand'),
    path('add_car/', AddCarView.as_view(), name='add_cars'),
    path('add_color/', AddColorView.as_view(), name='add_color'),
]