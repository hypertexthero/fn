from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):       
    class Meta:
        model = Profile
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

# =todo: http://djangosnippets.org/snippets/1301/