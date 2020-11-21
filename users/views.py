from django.contrib import messages
from django.contrib.auth import login as login_action
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import RegistrationForm, LoginForm
from users.models import User


def register(request: WSGIRequest):
    if request.user.is_authenticated:
        return redirect(reverse('pages:index'))

    registration_form = RegistrationForm()

    if request.method == 'POST':
        registration_form = RegistrationForm(data=request.POST)

        if registration_form.is_valid():
            new_user: User = registration_form.instance
            new_user.save()

            messages.add_message(request, messages.SUCCESS, 'Votre inscription a bien été validée !')

            login_action(request, new_user)

            return redirect(reverse('pages:index'))

    return render(request, 'users/registration.html', {
        'form': registration_form,
        'active_menu': 'register',
    })


class LoginView(SuccessMessageMixin, BaseLoginView):
    template_name = 'users/login.html'
    success_url = '/'
    authentication_form = LoginForm
    success_message = 'Vous êtes maintenant connecté !'
