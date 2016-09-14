"""omnibadge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^users/', include('users.urls')),
    url(r'^transactions/', include('transactions.urls')),
    url(r'^documents/', include('documents.urls')),
    url(r'^companies/', include('companies.urls')),
    url(r'^services/', include('services.urls')),
    url(r'^admin/', admin.site.urls),

    # to login at the api html page
    # doc: http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#adding-login-to-the-browsable-api
    url(r'^api-auth/', include('rest_framework.urls',)),

]