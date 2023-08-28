from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        fields = (
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save()(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
