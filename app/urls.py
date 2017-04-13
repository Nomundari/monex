# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.Home.as_view(), name = 'home'),
   
    url(r'^register/$', views.Register.as_view(), name = 'register'),
    url(r'^login/$', views.LoginUser.as_view(), name = 'login'),
    url(r'^logout/$', views.LoginUser.logout, name = 'logout'),
    url(r'^pass_change/$', views.ChangeUserPass.as_view(), name = 'change_pass'),
    url(r'^forgot_pass/$', views.ForgotUserPass.as_view(), name = 'forgot_pass'),
    url(r'^reset_pass/$', views.ResetUserPass.as_view(), name = 'reset_pass'),
    url(r'^user/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.ActiveUser.as_view(), name = 'active_user'),
    url(r'^user/pass_forgot/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.ResetUserPass.as_view(), name = 'reset_user'),
]