from django.urls import path
from .views import (
    CarsListView, ColorDetailView, CarDetailView,
    UserRegisterView, UserLoginView, UserLogoutView, ProfileDetailView,
    SendEmailView, AddBrandView, AddCarView, AddColorView, BrandListView, BrandDetailView,
    BrandUpdateView, BrandDeleteView,
    CarUpdateView, CarDeleteView
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

    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),
    path('brands/<int:pk>/update/', BrandUpdateView.as_view(), name='update_brand'),
    path('brands/<int:pk>/delete/', BrandDeleteView.as_view(), name='delete_brand'),

    # Cars uchun update va delete yo‘llari
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='update_car'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='delete_car'),

]