from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField


class User(AbstractUser):
    email = EmailField(unique=True, error_messages={
        'unique': 'Un utilisateur avec cette adresse e-mail existe déjà.'
    })
