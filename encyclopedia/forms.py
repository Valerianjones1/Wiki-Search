from django import forms


class SearchBar(forms.Form):
    query = forms.CharField(max_length=100)
