from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from documents.serializers import DocumentSerializer
from documents.restpermissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.reverse import reverse

from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import DocPassport


# Traditional way:
#
# def index(request):
#     latest_user_list = User.objects.order_by('-date_registered')[:5]
#     context = {
#         'latest_user_list': latest_user_list,
#     }
#     return render(request, 'users/index.html', context)
#
#
# def detail(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     return render(request, 'users/detail.html', {'user': user})


# Generic views way:

class IndexView(generic.ListView):
    template_name = 'documents/index.html'
    context_object_name = 'latest_document_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return DocPassport.objects.order_by('-date_created')[:5]


class DetailView(generic.DetailView):
    model = DocPassport
    template_name = 'documents/detail.html'


# ====== APIS ======
# Doc: http://www.django-rest-framework.org/tutorial/3-class-based-views/#using-generic-class-based-views

class DocumentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all users, or create a new user.
    """
    queryset = DocPassport.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DocumentDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = DocPassport.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'transactions': reverse('transaction-list', request=request, format=format),
    })


class DocumentHighlight(generics.GenericAPIView):
    queryset = DocPassport.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        transaction = self.get_object()
        return Response(transaction.highlighted)