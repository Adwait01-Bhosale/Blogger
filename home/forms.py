from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model 
from .models import Image, BlogData
from django import forms 



class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2'] 
  
  
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("img",) 
        
class Update(forms.ModelForm):
    class Meta:
        model=BlogData
        fields=["domain",
                "title",
                "content"]