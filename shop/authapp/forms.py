import hashlib
import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.forms import TextInput

from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')
        widgets = {
            "username": TextInput(attrs={
                'class': 'user-input',
                'placeholder': 'My name is',
            }),
            "password": TextInput(attrs={
                'type': "password",
            })
        }

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-styling'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['style'] = 'color: #7f8084;'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if isinstance(data, int):
            if data < 18 or not isinstance(data, int):
                raise forms.ValidationError("Вы слишком молоды!")
        else:
            raise forms.ValidationError("Введите возраст!")
        return data

    def save(self):
        user = super(ShopUserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if isinstance(data, int):
            if data < 18 or not isinstance(data, int):
                raise forms.ValidationError("Вы слишком молоды!")
        else:
            raise forms.ValidationError("Введите возраст!")
        return data