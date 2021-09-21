from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class SellerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'S':
            return True
        else:
            response = {
                'success': 'False',
                'message': 'User is not a Seller.',
                'status_code': status.HTTP_403_FORBIDDEN
            }
            raise PermissionDenied(detail=response, code=status.HTTP_403_FORBIDDEN)


class ProductOwnerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        response = {
            'success': 'False',
            'message': 'User is not the owner of the product or There are No Products Matching your request',
            'status_code': status.HTTP_403_FORBIDDEN
        }
        if obj is None:
            raise PermissionDenied(detail=response, code=status.HTTP_403_FORBIDDEN)
        if request.user.role == 'S' and request.user == obj.sellerId:
            return True
        else:
            raise PermissionDenied(detail=response, code=status.HTTP_403_FORBIDDEN)