from django.contrib import messages
from django.contrib.auth import login as login_action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from rest_framework.status import HTTP_200_OK

from tasks.api.serializers import TaskExportSerializer
from tasks.models import Task
from users.forms import RegistrationForm, LoginForm, EmailModificationForm, PasswordModificationForm, PasswordResetForm, \
    SetPasswordForm
from users.models import User


def register(request: WSGIRequest, *args, **kwargs):
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


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    success_url = '/'
    authentication_form = LoginForm


@login_required
def my_data(request: WSGIRequest, *args, **kwargs):
    return render(request, 'users/my_data.html', {
        'active_menu': 'users',
    })


@login_required
def download_my_data(request: WSGIRequest, *args, **kwargs):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskExportSerializer(tasks, many=True)

    response = HttpResponse(serializer.data, status=HTTP_200_OK)
    response['Content-Disposition'] = 'attachment; filename=mes-donnes-afaire.json'

    return response


@login_required
def my_information(request: WSGIRequest, *args, **kwargs):
    email_form = EmailModificationForm()
    password_form = PasswordModificationForm(user=request.user)

    return render(request, 'users/my_information.html', {
        'email_form': email_form,
        'password_form': password_form,
        'active_menu': 'users',
    })


@login_required
@require_POST
def update_email(request: WSGIRequest, *args, **kwargs):
    email_form = EmailModificationForm(data=request.POST, instance=request.user)

    if email_form.is_valid():
        email_form.save()

        messages.add_message(request, messages.SUCCESS, 'Votre e-mail a bien été modifié !')

        return redirect(reverse('users:my-information'))

    return render(request, 'users/my_information.html', {
        'email_form': email_form,
        'password_form': PasswordModificationForm(user=request.user),
        'active_menu': 'users',
    })


@login_required
@require_POST
def update_password(request: WSGIRequest, *args, **kwargs):
    password_form = PasswordModificationForm(data=request.POST, user=request.user)

    if password_form.is_valid():

        request.user.set_password(password_form.cleaned_data['new_password1'])
        request.user.save()

        messages.add_message(request, messages.SUCCESS, 'Votre mot de passe a bien été modifié !')

        login_action(request, request.user)

        return redirect(reverse('users:my-information'))

    return render(request, 'users/my_information.html', {
        'password_form': password_form,
        'email_form': EmailModificationForm(),
        'active_menu': 'users',
    })


class ResetPassword(PasswordResetView):
    template_name = 'users/reset-password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:reset-password-done')
    html_email_template_name = 'users/reset-password-email.html'
    email_template_name = 'users/reset-password-email.html'


class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'users/reset-password-done.html'


class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name = 'users/reset-password-confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('users:reset-password-complete')


class ResetPasswordComplete(PasswordResetCompleteView):
    template_name = 'users/reset-password-complete.html'
