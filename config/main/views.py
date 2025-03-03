from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Brands, Cars, Color, Comment, Profile
from .form import CarsForm, BrandsForm, ColorForm, CommentFrom, RegisterForm, LoginForm, SendEmail

# 1. Mashinalar ro'yxati
class CarsListView(ListView):
    model = Cars
    template_name = "cars_list.html"
    context_object_name = "cars"

# 2. Mashinalarni rang bo‘yicha filtrlash
class ColorDetailView(DetailView):
    model = Color
    template_name = "color_cars.html"
    context_object_name = "color"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Cars.objects.filter(color=self.object)
        context['all_color'] = Color.objects.all()
        return context

# 3. Mashinalarni brand bo‘yicha filtrlash
class BrandDetailView(DetailView):
    model = Brands
    template_name = "brand_cars.html"
    context_object_name = "brand"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Cars.objects.filter(brand=self.object)
        context['all_brands'] = Brands.objects.all()
        return context

# 4. Mashina tafsilotlari va izohlar
class CarDetailView(DetailView, FormView):
    model = Cars
    template_name = "car_detail.html"
    context_object_name = "car"
    form_class = CommentFrom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(car=self.object)
        return context

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        action = request.POST.get("action")
        if action == "create":
            form = self.get_form()
            if form.is_valid():
                review = form.save(commit=False)
                review.car = car
                review.user = request.user
                review.save()
            return redirect("car_detail", pk=car.id)
        elif action in ["update", "delete"]:
            review_id = request.POST.get("review_id")
            review = get_object_or_404(Comment, id=review_id, car=car)
            if request.user == review.user:
                if action == "update":
                    review.text = request.POST.get("text")
                    review.save()
                elif action == "delete":
                    review.delete()
            return redirect("car_detail", pk=car.id)
        return self.get(request, *args, **kwargs)

# 5. Ro‘yxatdan o‘tish
class UserRegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"{user.username} muvaffaqiyatli qo'shildi! Iltimos, login qiling!")
        return redirect("user_login")

# 6. Login
class UserLoginView(FormView):
    template_name = "user_login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f"Xush kelibsiz {user.first_name} {user.last_name}")
        return redirect("index")

# 7. Logout
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.warning(request, "Siz akkauntni tark etdingiz!")
        return redirect("user_login")

# 8. Profil sahifasi
class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = Cars.objects.filter(author=self.object.user)
        return context

# 9. Email yuborish
class SendEmailView(FormView):
    template_name = "send_main.html"
    form_class = SendEmail

    def form_valid(self, form):
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        for user in User.objects.all():
            send_mail(
                subject=subject,
                message=message,
                from_email='rustamovasilbek1221@gmail.com',
                recipient_list=[user.email]
            )
        messages.success(self.request, "Xabar yuborildi!")
        return redirect("index")

# 10. Yangi brand qo‘shish
class AddBrandView(CreateView):
    model = Brands
    form_class = BrandsForm
    template_name = "add_brands.html"
    success_url = reverse_lazy("index")

# 11. Yangi mashina qo‘shish
class AddCarView(CreateView):
    model = Cars
    form_class = CarsForm
    template_name = "add_cars.html"
    success_url = reverse_lazy("brands_detail")

# 12. Yangi rang qo‘shish
class AddColorView(CreateView):
    model = Color
    form_class = ColorForm
    template_name = "add_color.html"
    success_url = reverse_lazy("index")
