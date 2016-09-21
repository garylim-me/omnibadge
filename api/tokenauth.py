from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import get_authorization_header
from rest_framework import parsers, renderers, exceptions, authentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from users import models as user_models


# This class authenticates user and authorizes them to use the right API calls
# Referenced from TokenAuthentication
class SessionTokenAuthentication(authentication.BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'
    model = user_models.SessionToken

    def get_model(self):
        return self.model

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    # Extracts string from header and passes token string to authenticate_credentials
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    # TODO: need to rewrite logic here!
    def authenticate_credentials(self, key):
        model = self.get_model()

        # see if token belongs to anyone; if linked to a user, continue
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid session token.'))

        # see if linked person is actually active
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        # return user and token model instace
        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword

# Contents adapted ObtainAuthToken
class ObtainSessionToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # TODO: currently implements get_or_create -- hence, not possible to create multiple tokens here
        token, created = user_models.SessionToken.objects.get_or_create(user=user)
        return Response({'token': token.key})


# Note: Transaction tokens are handled separately
# -- obtaining it is done by Transaction Manager, and "Auth" is done in permissions

