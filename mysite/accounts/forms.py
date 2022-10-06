from django import forms
from allauth.account.forms import SignupForm


class CustomUserCreationForm(SignupForm):

    email = forms.EmailField(max_length = 256)
    first_name = forms.CharField(max_length = 128)
    last_name = forms.CharField(max_length = 128)

    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.save()
        return user
