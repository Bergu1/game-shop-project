from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254)


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput,
        strip=False,
    )

    def save(self, commit=True):

        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user