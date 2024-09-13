from home.models import Tweet
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class TweetForm(forms.ModelForm):
    
    class Meta:
        model = Tweet
        fields =["title","desc","image"]

class UserRegistraionForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Corrected this line
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})