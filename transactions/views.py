from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework import status, exceptions
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

from .models import Transaction
from api.tokenauth import SessionTokenAuthentication
from transactions.serializers import TransactionSerializer, TransactionCreateSerializer
from transactions.restpermissions import HasPrivilegesOrNoAccess


class IndexView(generic.ListView):
    template_name = 'transactions/index.html'
    context_object_name = 'latest_transaction_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Transaction.objects.order_by('-date_created')[:5]


class DetailView(generic.DetailView):
    model = Transaction
    template_name = 'transactions/detail.html'


# ====== APIS ======
# Doc: http://www.django-rest-framework.org/tutorial/3-class-based-views/#using-generic-class-based-views
class TransactionList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = (SessionTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, format=None):

        # TODO: permissions are actually spilling over here.
        # TODO: Maybe just create a class in restpermissions.py and call the class here.
        if request.auth is None:
            msg = "Invalid token header. No credentials provided."
            raise exceptions.AuthenticationFailed(msg)
        if request.auth.privilege.all_read:
            transactions = Transaction.objects.all()
        elif request.auth.privilege.company_read_transactions:
            transactions = Transaction.objects.filter(company=request.user.company)
        elif request.auth.privilege.user_read:
            transactions = Transaction.objects.filter(user=request.user)
        else:
            transactions = None

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            # Note: Can't return serializer.data because listed data don't actually belong to object
            # TODO: better fix needed
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = (SessionTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, HasPrivilegesOrNoAccess,)

    def get(self, request, *args, **kwargs):
        print "entering get"
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TransactionHighlight(generics.GenericAPIView):
    queryset = Transaction.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        transaction = self.get_object()
        return Response(transaction.highlighted)