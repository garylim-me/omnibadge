from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'companies'
urlpatterns = [

    # Generic views way:
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # APIs
    url(r'^api/$', views.CompanyList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.CompanyDetail.as_view()),

    url(r'^api/(?P<pk>[0-9]+)/highlight/$', views.CompanyHighlight.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)