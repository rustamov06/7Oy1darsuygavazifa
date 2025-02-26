from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from .models import Brands, Cars, Color, Comment, Profile
from django.contrib.auth.models import User
from .form import CarsForm, BrandsForm, ColorForm, CommentFrom, RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages

# 1-view  asosiy sahifa uchun javob beradigan view

def index(request):
    brands = Brands.objects.all()
    cars = Cars.objects.all()
    color = Color.objects.all()
    context = {
        'brands': brands,
        'cars': cars,
        'color': color
    }
    return render(request, 'index.html', context)


# 2-view     carlarni color bo'yicha salovchi



def color_detail(request, color_id):
    color = get_object_or_404(Color, id=color_id)
    cars = Cars.objects.filter(color=color)
    all_color = Color.objects.all()
    context = {
        'color': color,
        'cars': cars,
        'all_color': all_color
    }
    return render(request, 'color_cars.html', context)


# 3-view        carlarni brand bo'yicha saralovchi

def brand_detail(request, brand_id):
    brand = get_object_or_404(Brands, id=brand_id)
    cars = Cars.objects.filter(brand=brand)
    all_brands = Brands.objects.all()
    context = {
        'brand': brand,
        'cars': cars,
        'all_brands': all_brands
    }
    return render(request, 'brand_cars.html', context)


# 4 view      carni batafsil chiqaruvchi
# 5 view     car uchun comment qo'shuvchi

@permission_required('main.view_car', raise_exception=True)
def car_detail(request, car_id):
    """Mashina sahifasini ko‘rsatish va sharhlarni boshqarish"""
    car = get_object_or_404(Cars, id=car_id)
    comment = Comment.objects.filter(car=car)
    form = CommentFrom()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            form = CommentFrom(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.car = car
                review.user = request.user
                review.save()
            return redirect("car_detail", car_id=car.id)

        elif action == "update":
            review_id = request.POST.get("review_id")
            review = get_object_or_404(Comment, id=review_id, car=car)

            if request.user == review.user:
                review.text = request.POST.get("text")
                review.save()

            return redirect("car_detail", car_id=car.id)

        elif action == "delete":
            review_id = request.POST.get("review_id")
            review = get_object_or_404(Comment, id=review_id, car=car)
            if request.user == review.user:
                review.delete()

            return redirect("index")

    context = {
        "car": car,
        "comments": comment,
        "form": form
    }
    return render(request, "car_detail.html", context)



# 6 view          registratsiya uchun


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"{user.username} muofiqiyatli qo'shildi !\n"
                                      "Iltimos login qiling !")
            return redirect("user_login")

    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


# 7 view      login uchun

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz {user.first_name} {user.last_name}")
            return redirect('index')
    else:
        form = LoginForm()
    context = {
        'form' : form
    }

    return render(request, 'user_login.html', context)

# 8 view   logout uchun


@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, f"Siz akoutni tark etingiz janob !")
    return redirect("user_login")

def profile(request, username):

    context = {}
    try:
        user = get_object_or_404(User, username=username)
        car = Cars.objects.filter(author=user)
        profile = get_object_or_404(Profile, user=user)
        context['profile'] = profile
        context['car'] = car
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('index')
    return render(request, "profile.html", context)