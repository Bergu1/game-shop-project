from django import forms

class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"}),
    )