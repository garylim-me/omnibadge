from documents.serializers import DocumentSerializer, UserDocumentSerializer, CreateDocumentSerializer
from documents.restpermissions import HasTransTokenOrReadOnly, HasReadPriviledgesOrNoReadAccess, IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, generics, permissions, renderers
from django.views import generic

from .models import DocPassport, UserDocument


# Generic views way:
class IndexView(generic.ListView):
    template_name = 'documents/index.html'
    context_object_name = 'latest_document_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return UserDocument.objects.order_by('-id')[:5]


class DetailView(generic.DetailView):
    model = UserDocument
    template_name = 'documents/detail.html'


# ====== APIS ======
# Doc: http://www.django-rest-framework.org/tutorial/3-class-based-views/#using-generic-class-based-views

class DocumentList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    permission_classes = (HasReadPriviledgesOrNoReadAccess, HasTransTokenOrReadOnly)

    def get(self, request, format=None):
        snippets = UserDocument.objects.all()
        serializer = UserDocumentSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'creating serial'

        # Adding request user into data as creator
        # request.data['creator'] = 'self.request.user'

        serializer = CreateDocumentSerializer(data=request.data)
        print 'finished creating serial'
        if serializer.is_valid():
            print 'saving'
            serializer.save()
            print 'saved'
            # Note: Can't return serializer.data because listed data don't actually belong to object
            # TODO: better fix needed
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    """
    Retrieve, update or delete a document instance.
    """
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, HasReadPriviledgesOrNoReadAccess, IsOwnerOrReadOnly)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DocumentHighlight(generics.GenericAPIView):
    queryset = DocPassport.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        transaction = self.get_object()
        return Response(transaction.highlighted)