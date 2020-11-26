from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, \
    PasswordResetForm as BasePasswordResetForm, SetPasswordForm as BaseSetPasswordForm
from django.forms import EmailField, ModelForm
from django.urls import reverse

from users.models import User


class RegistrationForm(UserCreationForm):
    email = EmailField(required=True, error_messages={
        'unique': 'Cet email est déjà utilisé.',
    })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Je m\'inscris'))


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Connexion'))


class EmailModificationForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Je change mon email'))
        self.helper._form_action = reverse('users:update-email')


class PasswordModificationForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Je change mon mot de passe'))
        self.helper._form_action = reverse('users:update-password')


class PasswordResetForm(BasePasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Réinitialisation'))


class SetPasswordForm(BaseSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Celui-là, je le retiens ! 💪'))
