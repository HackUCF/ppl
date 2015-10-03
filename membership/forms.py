from django import forms


class SearchForm(forms.Form):
    knights_email = forms.CharField(required=True, min_length=2)
