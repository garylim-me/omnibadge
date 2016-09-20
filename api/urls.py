from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as auth_views
from . import views

from companies import views as company_views
from documents import views as document_views
from transactions import views as transaction_views
from users import views as user_views


app_name = 'api'
urlpatterns = [

    # APIs
    url(r'^companies/$', company_views.CompanyList.as_view(), name='company-list'),
    url(r'^companies/(?P<pk>[0-9]+)/$', company_views.CompanyDetail.as_view(), name='company-detail'),

    url(r'^documents/$', document_views.DocumentList.as_view(), name='document-list'),
    url(r'^documents/(?P<pk>[0-9]+)/$', document_views.DocumentDetail.as_view(), name='document-detail'),

    url(r'^transactions/$', transaction_views.TransactionList.as_view(), name='transaction-list'),
    url(r'^transactions/(?P<pk>[0-9]+)/$', transaction_views.TransactionDetail.as_view(), name='transaction-detail'),

    url(r'^users/$', user_views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_views.UserDetail.as_view(), name='user-detail'),

    url(r'^api-token-auth/', auth_views.obtain_auth_token),

    url(r'^root/$', views.api_root),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),



]

urlpatterns = format_suffix_patterns(urlpatterns)