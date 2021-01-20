from django import forms
from .models import User, UserFiles, FileComments, UserEmail
from django.core import validators
from django.core.exceptions import ValidationError


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators = [validators.MinLengthValidator(6)])
    password1 = forms.CharField()
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password1')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")
        if password != password1:
            raise ValidationError(
                    "Passowrd do not match "
                )

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserEmailForm(forms.ModelForm):

    class Meta:
        model = UserEmail
        fields = ('email', 'primary')


class UserFilesForm(forms.ModelForm):

    class Meta:
        model = UserFiles
        fields = ('files',)


class FileCommentsForm(forms.ModelForm):

    class Meta:
        model = FileComments
        fields = ('comments',)        