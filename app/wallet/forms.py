from django import forms

class AmountForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=0.01, 
        label="Enter the amount you want to deposit:",
        widget=forms.NumberInput(attrs={'class': 'amount-input', 'placeholder': 'Enter amount'})
    )
