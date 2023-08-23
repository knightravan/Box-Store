from django import forms
from .models import box 
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField
from django.contrib.auth.models import User

class signupform(UserCreationForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))


	class Meta:
		model=User
		fields=['id','username', 'first_name','last_name','email']
		labels={'first_name':"First Name",'last_name':"Last Name", 'email':"Email"}
		widgets={'username':forms.TextInput(attrs={'class':'form-control'}),
				'first_name':forms.TextInput(attrs={'class':'form-control'}),
				'last_name':forms.TextInput(attrs={'class':'form-control'}),
				'email':forms.EmailInput(attrs={'class':'form-control'})
			}

class Loginform(AuthenticationForm):
	username= UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
	password = forms.CharField( label=_("Password"), strip=False, widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))



class PostForm(forms.ModelForm):
	class Meta:
		model = box
		fields=['length','breadth','height','creator']
		labels={'length':'Length','breadth':'Breadth','height':'Height'}	
		widgets={'length':forms.NumberInput(attrs={'class':'form-control'}),
				'breadth':forms.NumberInput(attrs={'class':'form-control'}),
				'height':forms.NumberInput(attrs={'class':'form-control'}),
				}
