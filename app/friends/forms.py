from django import forms
from coredb.models import Person

class FriendForm(forms.Form):
    recipient_username = forms.CharField(max_length=150, label="Recipient Username")

    def clean_recipient_username(self):
        username = self.cleaned_data['recipient_username']
        try:
            recipient = Person.objects.get(username=username)
        except Person.DoesNotExist:
            return None
        return recipient
