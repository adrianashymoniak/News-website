from django.contrib.auth.forms import UserCreationForm
from django import forms

from news.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True,
                             help_text='Required. Inform a valid email '
                                       'address')
    username = forms.CharField(max_length=150, required=False,
                               help_text='Optional')
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional')
    last_name = forms.CharField(max_length=200, required=False,
                                help_text='Optional')
    date_of_birth = forms.DateField(required=False, help_text='Optional')

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'date_of_birth',
            'password1',
            'password2',
        )
