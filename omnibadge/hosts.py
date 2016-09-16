from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
                         host(r'www', settings.ROOT_URLCONF, name='www'),
                         host(r'api', 'api.urls', name='api'),
                         # host(r'beta', 'beta.urls', name='beta'),
                         )

'''
To test in localhost, try:
http://api.127.0.0.1.xip.io:8000/users/1/
'''