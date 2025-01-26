from django import forms 
from .models import Posts


class Add_Post(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title','content']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control',
                                        'placeholder':'Enter the topic of the post'}),
            'content': forms.Textarea(attrs={'class':'form-control',
                                        'placeholder':'Write your post here'}),
        }
        

from django.contrib.auth.models import User
from .models import Profile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'about']
