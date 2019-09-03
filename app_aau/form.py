from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms
from app_aau.models import *

"""
malhar_email
"""
class UserSignForm(UserCreationForm):

    class Meta:
        fields=("email","password1","password2")
        model=get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].label="Your Email Address"


###############################################

# class UserSignForm(UserCreationForm):
#
#     class Meta:
#         fields=("email","password1","password2")
#         model=get_user_model()
#
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         # self.fields['username'].label="Display Name"
#         self.fields['email'].label="Your Email Address"
######################################################


class File_Upload(forms.ModelForm):

    class Meta:
        fields=("file_path",)
        model=TempFile

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['file_path'].label=""




class Password_change_Form(forms.ModelForm):

    password=forms.CharField(label="Enter New Password",widget=forms.PasswordInput(
        attrs={
        "placeholder":'Enter New Password',
        "class":"form-control"
        }
    ))
    class Meta():
        model=get_user_model()
        fields=('password',)  #,'email')


class RegistrarUploadFile(forms.Form):
    file = forms.FileField(label="")


class Reject_reason_Form(forms.Form):
    reject_message = forms.CharField(
        max_length=130,
        label="Reason"
    )
