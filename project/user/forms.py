from django import forms
from .models import people,complaints
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class customUserCreationForm(UserCreationForm):
    first_name=forms.CharField(max_length=100,required=True)
    last_name=forms.CharField(max_length=100,required=True)
    email=forms.EmailField(required=True)
    class  Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
        labels={'username':'Username','first_name':'First Name','last_name':'Last Name','email':'Email'}
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'})
        }
        
class peopleForm(forms.ModelForm):
    class Meta:
        model=people
        fields=['collegename','contactnumber','Branch'] 
        labels={'collegename':'College Name','contactnumber':'Contact Number','Branch':'Branch'}
        widgets={
            'collegename':forms.Select(attrs={'class':'form-control'}),
            'contactnumber':forms.TextInput(attrs={'class':'form-control'}),
            'Branch':forms.Select(attrs={'class':'form-control'})
        }
class complaintForm(forms.ModelForm):
    class Meta:
        model=complaints
        fields=['subject','type','description']
        labels={'subject':'Subject','type':'Type','description':'Description'}
        widget={
            'subject':forms.TextInput(attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'})
        }
class ProfileUpdateForm(forms.ModelForm):
    collegename =forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    Branch=forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model=people
        fields=['collegename','contactnumber','Branch']
        labels={'collegename':'College Name','contactnumber':'Contact Number','Branch':'Branch'}
        widgets={
            'collegename':forms.Select(attrs={'class':'form-control'}),
            'contactnumber':forms.TextInput(attrs={'class':'form-control'}),
            'Branch':forms.Select(attrs={'class':'form-control'})
        }       
class userprofileupdate(forms.ModelForm):
    username=forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    email =forms.EmailField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    first_name=forms.CharField( max_length=30, required=True)
    last_name=forms.CharField( max_length=30, required=True)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
        labels = {'username':'Username','email':'Email','first_name':'First Name','last_name':'Last Name'}
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'})
        }
class statusupdate(forms.ModelForm):
    class Meta:
        model=complaints
        fields=('status',)  
        help_texts = {
            'status': None,
        }