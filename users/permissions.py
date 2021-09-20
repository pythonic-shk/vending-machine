from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class BuyerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'B':
            return True
        else:
            response = {
                'success': 'False',
                'message': 'User is Not a Buyer',
                'status_code': status.HTTP_401_UNAUTHORIZED
            }
            raise PermissionDenied(detail=response, code=status.HTTP_401_UNAUTHORIZED)




