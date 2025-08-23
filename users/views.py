from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from users.forms import UserRegisterForm, UserLoginForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        send_mail(
            "Добро пожаловать в Skystore!",
            "Вы успешно зарегистрировались в нашем магазине.",
            "from@example.com",
            [user.email],
            fail_silently=False,
        )
        login(self.request, user)
        return response


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
