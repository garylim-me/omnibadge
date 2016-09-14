from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'documents'
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
    url(r'^api/$', views.DocumentList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.DocumentDetail.as_view()),

    url(r'^api/root$', views.api_root),
    url(r'^api/(?P<pk>[0-9]+)/highlight/$', views.DocumentHighlight.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)