from django.urls import reverse_lazy

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.contrib import messages
from .forms import CustomPasswordResetForm, SetPasswordForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'resetpassbymail/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'resetpassbymail/password_reset_email.html'  
    subject_template_name = 'resetpassbymail/password_reset_subject.txt'  


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'resetpassbymail/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = 'resetpassbymail/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'resetpassbymail/password_reset_complete.html'