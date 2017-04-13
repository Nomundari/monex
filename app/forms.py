# -*- coding:utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
import re
class RegisterForm(forms.Form):
	lastname = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':u'Овог'}))
	firstname = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':u'Нэр'}))
	username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':u'Нэвтрэх Нэр'}))
	email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control', 'placeholder':u'И-майл хаяг'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':u'Нууц үг'}))
	
class LoginForm(forms.Form):
	username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':u'Нэвтрэх Нэр'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':u'Нууц үг'}))

class ChangeUserPassForm(forms.Form):
	old_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Хуучин нууц үг'}))
	new_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг'}), min_length=7, validators=[RegexValidator('^[A-Za-z0-9]+$', message="Password should be a combination of Alphabets and Numbers")])
	repeat_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг давтах'}), min_length=7, validators=[RegexValidator('^[A-Za-z0-9]+$', message="Password should be a combination of Alphabets and Numbers")])
	def clean(self):
		cleaned_data = super(ChangeUserPassForm, self).clean()
		if self.is_valid():
			if len(cleaned_data['new_password'])<8:
				raise forms.ValidationError(u'Таны оруулсан нууц үг хамгийн багадаа наймын урттай байх шаардлагатай')
			if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&.])[A-Za-z\d$@$!%*?&.]+$", cleaned_data['new_password']):
				raise forms.ValidationError("Таны нууц үг үсэг, тооноос бүрдсэн байх шаардлагатай")
			if cleaned_data['old_password'] == cleaned_data['new_password']:
				raise forms.ValidationError(u'Шинэ нууц хуучин нууц үгтэй ижил байна. Өөр нууц үг хийнэ үү')
			if cleaned_data['new_password'] != cleaned_data['repeat_password']:
				raise forms.ValidationError(u'Шинэ нууц үг таарахгүй байна')
		return cleaned_data

class CheckEmailForm(forms.Form):
	email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control', 'placeholder':u'И-майл хаяг'}))

class ResetUserPassFrom(forms.Form):
	new_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг'}))
	repeat_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг давтах'}))
	def clean(self):
		cleaned_data = super(ChangeUserPassForm, self).clean()
		if self.is_valid():
			if cleaned_data['old_password'] == cleaned_data['new_password1']:
				raise forms.ValidationError(u'Шинэ нууц хуучин нууц үгтэй ижил байна. Өөр нууц үг хийнэ үү')
			if cleaned_data['new_password1'] != cleaned_data['new_password2']:
				raise forms.ValidationError(u'Шинэ нууц үг таарахгүй байна')
		return cleaned_data
