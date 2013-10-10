# from django import forms
# from mezzanine.accounts.forms import ProfileForm
# from .models import Profile
# from django.contrib.auth.models import User
# 
# class MyProfileForm(ProfileForm):       
#     class Meta:
#         # fields = ['username', 'website', 'bio']
#         # exclude = {'password1', 'password2'}
#         widgets = {
#             'password1': forms.HiddenInput(),
#             'password1': forms.HiddenInput()
#         }
#         
#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)
#         del self.fields['password1']
#         del self.fields['password2']
# 
# 
# 
# # =todo: http://djangosnippets.org/snippets/1301/