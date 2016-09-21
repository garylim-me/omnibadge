from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api.tokenauth import ObtainSessionToken
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

    # APIs
    url(r'^api/$', views.UserList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    url(r'^api/(?P<pk>[0-9]+)/highlight/$', views.UserHighlight.as_view()),

    url(r'^api-token-auth/', ObtainSessionToken.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)