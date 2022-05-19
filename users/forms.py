from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields + ('email','avatar')
    


class LoginForm(forms.Form):
    email=forms.EmailField()
    password= forms.CharField(widget=forms.PasswordInput)
    

    def clean(self):
        email=self.cleaned_data.get("email")
        password=self.cleaned_data.get("password")
        try:
            user=models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("password wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exits!"))