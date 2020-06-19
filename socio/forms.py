from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Comment,checkmk

class UserRegisterForm(UserCreationForm):
	email=forms.EmailField(required=True)
	first_name=forms.CharField(max_length=100,required=True)
	last_name=forms.CharField(max_length=100,required=True)

	class Meta:
		model=User
		fields=['username','first_name','last_name','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']

class checkimage(forms.ModelForm):

    class Meta:
        model=checkmk
        fields=['d_image']


class CommentForm(forms.ModelForm):
    content=forms.CharField(label="",widget=forms.Textarea(
    attrs={
        'class':'form-control',
        'placeholder':'Comment here!',
        'rows':4,
        'cols':50
    }))
    class Meta:
        model = Comment
        fields=['content']
        