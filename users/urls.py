from django.conf.urls import url

from . import views


app_name = 'users'
urlpatterns = [

    # Traditional way:
    # # ex: /users/
    # url(r'^$', views.index, name='index'),
    # # ex: /users/5/
    # url(r'^(?P<user_id>[0-9]+)/$', views.detail, name='detail'),

    # Generic views way:
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

]