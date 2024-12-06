from django import forms
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']






class SearchForm(forms.Form):
    
    """A form for capturing search criteria to filter news articles.
    This form is used to gather search parameters from the user, including the search keyword,
    date range, source, language, and category. The form supports optional fields for start date, 
    end date, source, language, and category, while the keyword field is required
    """
    keyword = forms.CharField(max_length=100, required=True)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    source_name = forms.CharField(max_length=100, required=False)
    language_name = forms.CharField(max_length=50, required=False)
    category_name = forms.CharField(max_length=50, required=False)




    
    