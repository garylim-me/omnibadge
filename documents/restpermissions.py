# created for REST APIs
# doc: http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#object-level-permissions
# #notsurewhycan'tnameaspermissions

from rest_framework import permissions


# TODO: Check if owner, else can't modify? Think about it.
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Not going to discriminate between actions
        if request.method in permissions.SAFE_METHODS:
            pass
            # return True

        # Write permissions are only allowed to the owner of the snippet.
        # NOTE: the obj.user refers to the "user" column in the UserDocument table
        return obj.user == request.user


# TODO: verify business logic
class HasTransTokenOrReadOnly(permissions.BasePermission):
    """
    For creating new documents -- need to supply transaction token!
    Compares document's transaction_token to the one supplied in the header

    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.document_object.transaction.transaction_token_id == request.POST.get('transaction_token', '')


# TODO: Code here is broken
class HasReadPriviledgesOrNoReadAccess(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # TODO: Check if owner or if company can see
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.transaction_token_id == request.POST.get('transaction_token', '')
