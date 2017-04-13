# -*- coding:utf-8 -*-
import managers
import forms as f
import datetime
import session
import urllib
from django.shortcuts import render
from django.views import generic as g
from django.core.urlresolvers import reverse_lazy
from django.forms.utils import ErrorList
from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.conf import settings



class User(object):
	pk = None
	last_login = None
	password = None


	def is_authenticated(self):
		return True
	def is_user(self):
		return True
class LoginRequired(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user is None:
			next_url = urllib.urlencode({'next': request.get_full_path()})
			return redirect('%s?%s' % (reverse_lazy('login'), next_url))
		return super(LoginRequired, self).dispatch(request, *args, **kwargs)


	
class Home(g.TemplateView):
	template_name = 'base.html'
	
	#def get_context_data(self, **kwargs):
	#	context = super(Home, self).get_context_data(**kwargs)
	#	managers.BaseDataManager.register()
	#	print "##############"
	#	return context

class Register(g.FormView):
	form_class = f.RegisterForm
	template_name = 'register.html'
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		firstname = form.cleaned_data['firstname']
		lastname = form.cleaned_data['lastname']
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		date_joined = datetime.now().strftime('%Y-%m-%d %H:%M:%S%z')
		result = managers.BaseDataManager.register(firstname, lastname, username, email, password, date_joined)
		if result.isUsernameDuplicated:
			form._errors["__all__"] = ErrorList([u'Нэвтрэх нэр бүртгэлтэй байна.'])
			return super(Register, self).form_invalid(form)
		if result.isEmailDuplicated:
			form._errors["__all__"] = ErrorList([u'И-майл бүртгэлтэй байна.'])
			return super(Register, self).form_invalid(form)
		#000make token
		print "**************"
		print "**************"
		print "**************"
		print result.id
		print result.password
		print "**************"
		print "**************"

		user = User()
		user.pk = result.id.value
		if hasattr(result.last_login, 'value'):
			dt = result.last_login.value.split('.')[0]
			user.last_login = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
		user.password = result.password.value
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		link = 'http://localhost:8000/user/reset/%s/%s/' %(uid, token)
		subject= u'Та доорх link-р орж бүртгэлээ баталгаажуулна уу\n'
		result = managers.BaseDataManager.send_email(email, link, subject)

		return super(Register, self).form_valid(form)
	


class ActiveUser(g.TemplateView):
	template_name = 'validlink.html'
	def dispatch(self, request, *args, **kwargs):
		print kwargs['uidb64']
		iid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
		itoken = kwargs['token']
		result = managers.BaseDataManager.get_user(iid)
		
		user = User()
		user.pk = result.id.value
		if hasattr(result.last_login, 'value'):
			dt = result.last_login.value.split('.')[0]
			user.last_login = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
		#user.last_login = ll
		user.password = result.password.value
		token = default_token_generator.make_token(user)		
		if (token==itoken):
			result1 = managers.BaseDataManager.is_active('1', iid)

		else:
			raise Http404
		return super(ActiveUser, self).dispatch(request, *args, **kwargs)

class LoginUser(g.FormView):
	form_class = f.LoginForm
	template_name = 'login.html'
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		username=form.cleaned_data['username']
		password=form.cleaned_data['password']
		last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		result=  managers.BaseDataManager.login(username, password, last_login)
		user = User()
		user.pk=result.id.value
		if result.isValidUser == False:
			form._errors['__all__'] = u'Хэрэглэгч нэр эсвэл нууц үг буруу байна'
			return super(LoginUser, self).form_invalid(form)
		else:
			if result.isActive == 0:
				form._errors['__all__'] = u'Хэрэглэгчийн хандах эрх цуцлагдсан байна.'
				return super(LoginUser, self).form_invalid(form)
			else:
				session.put(self.request, 'user', user)
				return super(LoginUser, self).form_valid(form)
				#return render(self.request, 'base.html', {"user" :user})
				#print user
	@staticmethod
	def logout(request):
		session.pop(request, 'user')
		return HttpResponseRedirect(reverse_lazy('home'))
		
class ChangeUserPass(LoginRequired, g.FormView):
	form_class = f.ChangeUserPassForm
	template_name = "pass_change.html"
	success_url  = reverse_lazy('home')
	def form_valid(self, form):
		user = session.get(self.request, 'user')
		id=user.pk
		currentPassword = form.cleaned_data['old_password']
		newPassword = form.cleaned_data['new_password1']
		result = managers.BaseDataManager.change_password(id ,currentPassword, newPassword)
		print result
		if result.currentPasswordIsValid == False:
			form._errors['__all__'] = u'Хуучин нууц үг таарахгүй байна'
			return super(ChangeUserPass, self).form_invalid(form)
		return super(ChangeUserPass, self).form_valid(form)

class ForgotUserPass(g.FormView):
	form_class = f.CheckEmailForm
	template_name = "check_email.html"
	success_url  = reverse_lazy('home')
	def form_valid(self, form):
		email = form.cleaned_data['email']
		result = managers.BaseDataManager.check_email(email)
		user = User()
		user.pk = result.id.value
		if hasattr(result.last_login, 'value'):
			print result.last_login.value.split('.')
			dt = result.last_login.value.split('.')[0]
			user.last_login = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
		user.password = result.password.value
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		link = 'http://localhost:8000/user/pass_forgot/%s/%s/' %(uid, token)
		subject= u'Та доорх link-р орж нууц үгээ солино уу\n'
		sending = managers.BaseDataManager.send_email(email, link, subject)
		return super(ForgotUserPass, self).form_valid(form)

class ResetUserPass(g.TemplateView):
	template_name = 'valid.html'
	form_class = f.ResetUserPassFrom
	success_url  = reverse_lazy('reset_pass')
	def dispatch(self, request, *args, **kwargs):
		print kwargs['uidb64']
		iid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
		print iid
		result = managers.BaseDataManager.insert_pass(iid)
		return super(ActiveUser, self).dispatch(request, *args, **kwargs)