from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'companies': reverse('company-list', request=request, format=format),
        'documents': reverse('document-list', request=request, format=format),
        'transactions': reverse('transaction-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })
