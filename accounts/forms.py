# /Users/keinagai/Desktop/mystudy/EldergateLibrary/accounts/forms.py

from django import forms
from django.contrib.auth.hashers import make_password
from .models import EldergateLibraryUser

class ReaderSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = EldergateLibraryUser
        fields = ['First_Name', 'Last_Name', 'username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        user.model_name = 'Reader'
        if commit:
            user.save()
        return user


class ReaderProfileEditForm(forms.ModelForm):
    class Meta:
        model = EldergateLibraryUser
        fields = ['First_Name', 'Last_Name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

#####Librarian SignUp Form#####
class LibrarianSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = EldergateLibraryUser
        fields = ['First_Name', 'Last_Name', 'username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        user.model_name = 'Librarian'
        if commit:
            user.save()
        return user
