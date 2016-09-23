# created for REST APIs
# doc: http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#object-level-permissions
# #notsurewhycan'tnameaspermissions

from rest_framework import permissions


class HasPrivilegesOrNoAccess(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    # note: this is only run when querying for object details; not when listing objects.
    def has_object_permission(self, request, view, obj):

        print "entering has_object_permission"
        print request.auth
        print request.user

        # If read: check if owner. Else check appropriate read methods
        if request.method in permissions.SAFE_METHODS:

            return ((request.auth.privilege.user_read & (request.user == obj.user)) |  # if transaction belongs to user
                    request.auth.privilege.all_read |  # if admin read privilege
                    (request.auth.privilege.company_read_transactions &  # if company read, AND
                     (request.user.company == obj.company))  # if transaction belongs to company
                    )

        # Write permissions are only allowed to the owner of the snippet.
        return ((request.auth.privilege.user_write & request.user == obj.user) |  # if transaction belongs to user
                request.auth.privilege.all_write |  # if admin write privilege
                (request.auth.privilege.company_write_transactions &  # if company write, AND
                 request.user.company == obj.company)  # if transaction belongs to company
                )
