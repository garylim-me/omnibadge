from documents.serializers import DocumentSerializer, UserDocumentSerializer, CreateDocumentSerializer
from documents.restpermissions import HasTransTokenOrReadOnly, HasPrivilegesOrNoAccess
from rest_framework import status, exceptions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, generics, permissions, renderers

from django.views import generic

from api.tokenauth import SessionTokenAuthentication
from .models import DocPassport, UserDocument
from transactions.models import Transaction


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

    # standard session auth; returns request.user and request.auth
    authentication_classes = (SessionTokenAuthentication,)

    # To access documents, need read privileges (admin, company, user owns), also need to filter for docs that belong
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, HasTransTokenOrReadOnly)


    def get_company_documents(self, request):
        # get company id
        company = request.user.company

        # get company transactions
        transactions_list = Transaction.objects.filter(company=company)
        transactions_list_ids = [transaction.id for transaction in transactions_list]
        transactions_queryset = Transaction.objects.filter(id__in=transactions_list_ids)

        # Get user documents linked to the transaction set
        # note: using a set to remove duplicates
        user_documents = UserDocument.objects.filter(transactions__in=transactions_queryset).distinct()

        # get all documents under those transactions
        return user_documents

    def get(self, request, format=None):

        # TODO: permissions are actually spilling over here.
        # TODO: Maybe just create a class in restpermissions.py and call the class here.
        if request.auth is None:
            msg = "Invalid token header. No credentials provided."
            raise exceptions.AuthenticationFailed(msg)
        if request.auth.privilege.all_read:
            documents = UserDocument.objects.all()
        # TODO: THIS IS BROKEN!!
        elif request.auth.privilege.company_read_documents:
            documents = self.get_company_documents(request)
        elif request.auth.privilege.user_read:
            documents = UserDocument.objects.filter(user=request.user)
        else:
            documents = None
        #TEMP
        # documents = UserDocument.objects.all()
        serializer = UserDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'creating serial'
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

    # standard session auth; returns request.user and request.auth
    authentication_classes = (SessionTokenAuthentication, )

    # To access documents, need read privileges (admin, company, user owns), also need to filter for docs that belong
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, HasPrivilegesOrNoAccess, )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # this is not expected to be used. To review permissions and logic if opening up.
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

        # this is not expected to be used. To review permissions and logic if opening up.
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DocumentHighlight(generics.GenericAPIView):
    queryset = DocPassport.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        transaction = self.get_object()
        return Response(transaction.highlighted)