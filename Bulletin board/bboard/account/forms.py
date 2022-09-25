from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from allauth.account.forms import SignupForm
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class AuthorsSignupForm(SignupForm):

    def save(self, request):
        user = super(AuthorsSignupForm, self).save(request)
        authors_group = Group.objects.get(name='authors')
        authors_group.user_set.add(user)
        return user