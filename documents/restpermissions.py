# created for REST APIs
# doc: http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#object-level-permissions
# #notsurewhycan'tnameaspermissions
import json
from rest_framework import permissions, exceptions
from transactions.models import TransactionToken



# This is for list only -- post and edits
class HasTransTokenOrReadOnly(permissions.BasePermission):
    """
    For creating new documents -- need to supply transaction token!
    Compares document's transaction_token to the one supplied in the header

    """

    # TODO: not called yet. Also needs fixing
    # checks provided transaction token to created doc's token
    def transaction_tokens_match(self, document, request):
        return document.transactions.filter(transaction_token_id="123").count() > 0

    # check transaction token belongs to users's company
    # get transaction from token, check that transaction belongs to user's company
    # TODO: move to document creation check maybe?
    def valid_transaction_token(self, request):
        if request.method != "POST":
            return False
        else:
            transaction_token_string = json.loads(request.body)["transaction_token"]

            # check for valid token
            try:
                transaction_token = TransactionToken.objects.get(key=transaction_token_string)
            except:
                raise exceptions.AuthenticationFailed("Invalid transaction_token.")

            # check that transaction company is the same as user's
            if transaction_token.transaction.company != request.user.company:
                raise exceptions.AuthenticationFailed("This transaction doesn't belong to your company.")

            # TODO: When posting new documents, either state transaction_id, or state transaction_token.
            # TODO: NEED TO DECIDE! Current choice: transaction_token (remove transaction_id requirements for posts)
            # check that sent user email matches the transaction's user email (sanity check)
            email_string = json.loads(request.body)["email"]
            if transaction_token.transaction.user.email != email_string:
                raise exceptions.AuthenticationFailed("Provided email doesn't match the transaction's email")

            return True

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return self.valid_transaction_token(request)


# This is for details only
class HasPrivilegesOrNoAccess(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    # Checks the document's transactions for the user's company.
    def object_accessable_by_company(self, user, user_document):
        return user_document.transactions.filter(company=user.company).count() > 0

    # note: this is only run when querying for object details; not when listing objects.
    def has_object_permission(self, request, view, obj):

        # If read: check if owner. Else check appropriate read methods
        if request.method in permissions.SAFE_METHODS:

            return (
                # if transaction belongs to user
                (request.auth.privilege.user_read & (request.user == obj.user)) |
                request.auth.privilege.all_read |  # if admin read privilege
                (request.auth.privilege.company_read_documents &  # if company read, AND
                 self.object_accessable_by_company(request.user, obj))
            )

        # Write permissions are only allowed to the owner of the snippet.
        return ((request.user == obj.user) |  # if transaction belongs to user
                request.auth.privilege.all_write |  # if admin write privilege
                (request.auth.privilege.company_write_transactions &  # if company write, AND
                 (request.user.company == obj.company))  # if transaction belongs to company
                )
