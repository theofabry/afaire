from factory import DjangoModelFactory, Sequence, SubFactory
from rest_framework.authtoken.models import Token

from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence('user{0}'.format)
    email = Sequence('user{0}@gmail.com'.format)
    is_active = True


class TokenFactory(DjangoModelFactory):
    class Meta:
        model = Token

    user = SubFactory(UserFactory)

