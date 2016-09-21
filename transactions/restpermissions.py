# created for REST APIs
# doc: http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#object-level-permissions
# #notsurewhycan'tnameaspermissions

from rest_framework import permissions


class HasTransTokenOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.transaction_token_id == request.POST.get('transaction_token', '')


# TODO: rewrite for session token
class HasReadPrivilegesOrNoAccess(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        print request.auth
        print request.user

        # If read: check if owner. Else check appropriate read methods
        if request.method in permissions.SAFE_METHODS:

            return ((request.user == obj.user) |  # if transaction belongs to user
                    request.auth.privilege.all_read |  # if admin read privilege
                    (request.auth.privilege.company_read_transactions &  # if company read, AND
                     (request.user.company == obj.company))  # if transaction belongs to company
                    )

        # Write permissions are only allowed to the owner of the snippet.
        return (request.user == obj.user |  # if transaction belongs to user
                request.auth.privilege.all_write |  # if admin write privilege
                (request.auth.privilege.company_write_transactions &  # if company write, AND
                 request.user.company == obj.company)  # if transaction belongs to company
                )
