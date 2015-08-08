"""allsocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from allauth.account.views import logout

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/logout/$', 'allauth.account.views.LogoutView'),
    url(r'^disconnect/(?P<backend>[^/]+)/$', logout, name='socialauth_disconnect'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'testsocial.views.hello',name='hello'),
    url(r'^accounts/profile/$', 'testsocial.views.home',name='home'),
    url(r'^testlogout/$', 'testsocial.views.logout',name='testlogout'),
    url(r'^getusernames/$', 'testsocial.views.users',name='users'),
    url(r'^hello_world/$', 'django_twilio.views.say', {'text': 'Hello, world!'}),
    url(r'^play/$', 'django_twilio.views.play', {'url': 'http://mysite.com/greeting.wav',}),
    url(r'^gather/$', 'testsocial.views.gather_digits'),
    url(r'^respond/$', 'testsocial.views.handle_response'),
    url(r'^message/$', 'django_twilio.views.message', {
        'message': 'Yo!',
        'to': '+919440247341',
        'sender': '+18882223333',
        'status_callback': '/gather/$',
    }),
    url(r'^call/$', 'testsocial.views.callnumber'),
]
