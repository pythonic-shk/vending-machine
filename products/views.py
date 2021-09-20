from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import SellerOnly, ProductOwnerOnly
from users.permissions import BuyerOnly
from .serializers import ProductCreateSerializer, ProductDeleteSerializer,\
    ProductUpdateSerializer, ProductBuySerializer
from .models import Product
from users.models import Deposit

from users.models import Deposit


class ProductCreateView(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = (IsAuthenticated, SellerOnly,)

    def post(self, request):
        self.check_object_permissions(self.request, self.request.user)
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(sellerId=request.user)
            status_code = status.HTTP_201_CREATED
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Product created successfully',
            }

            return JsonResponse(response, status=status_code)
        except (ValidationError, ValueError, TypeError, IntegrityError) as msg:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'False',
                'status code': status_code,
                'message': str(msg),
            }
            return JsonResponse(response, status=status_code)


class ProductShowView(ListAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            response = {
                 'success': 'True',
                 'code': status.HTTP_202_ACCEPTED,
                 'message': 'Getting Products Successfully',
                 'data': list(Product.objects.all().values('productName', 'cost', 'amountAvailable', 'sellerId'))
             }
            return JsonResponse(response, status=status.HTTP_202_ACCEPTED, safe=False)
        except (ValueError, TypeError, AttributeError) as msg:
            response = {
                'success': 'False',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error with the request',
                'data': []
            }
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductUpdateView(UpdateAPIView):
    serializer_class = ProductUpdateSerializer
    permission_classes = (IsAuthenticated, ProductOwnerOnly)

    def update(self, request):
        try:
            try:
                prd = Product.objects.get(sellerId=request.user)
            except Product.DoesNotExist:
                prd = None
            self.check_object_permissions(self.request, prd)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid()
            prd.productName = serializer.data.get("productName")
            prd.cost = serializer.data.get("cost")
            prd.amountAvailable = serializer.data.get("amountAvailable")
            prd.save()
            status_code = status.HTTP_202_ACCEPTED
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Product updated successfully',
            }

            return JsonResponse(response, status=status_code)

        except (ValidationError, ValueError, TypeError, IntegrityError) as msg:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'False',
                'status code': status_code,
                'message': str(msg),
            }
            return JsonResponse(response, status=status_code)


class ProductDeleteView(DestroyAPIView):
    serializer_class = ProductDeleteSerializer
    permission_classes = (IsAuthenticated, ProductOwnerOnly)

    def delete(self, request):
        try:
            try:
                prd = Product.objects.get(sellerId=request.user)
            except Product.DoesNotExist:
                prd = None
            self.check_object_permissions(self.request, prd)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
            prd = Product.objects.filter(sellerId=request.user,
                                         productName=serializer.data.get("productName"))
            prd_name = prd.productName
            prd.delete()
            response = {
                'success': 'True',
                'code': status.HTTP_200_OK,
                'message': 'Product ' + prd_name + ' Deleted successfully',
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
        except (ValidationError, ValueError, TypeError) as msg:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'False',
                'status code': status_code,
                'message': str(msg),
            }
            return JsonResponse(response, status=status_code)


class ProductBuyView(UpdateAPIView):
    serializer_class = ProductBuySerializer
    permission_classes = (IsAuthenticated, BuyerOnly)

    def update(self, request):
        try:
            self.check_object_permissions(self.request, self.request.user)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid()
            dep = Deposit.objects.get(buyerId=request.user)
            try:
                prd = Product.objects.get(sellerId=serializer.data.get("sellerId"),
                                         productName=serializer.data.get("productName"))
            except Product.DoesNotExist:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': 'False',
                    'status code': status_code,
                    'message': 'Requested Product is not available',
                }
                return JsonResponse(response, status=status_code)
            if prd.amountAvailable < int(serializer.data.get("quantity")):
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': 'False',
                    'status code': status_code,
                    'message': 'Requested Quantity is not available',
                }
                return JsonResponse(response, status=status_code)
            elif dep.total < int(serializer.data.get("quantity")) * prd.cost:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': 'False',
                    'status code': status_code,
                    'message': 'Insufficient Funds',
                }
                return JsonResponse(response, status=status_code)
            else:
                prd.amountAvailable -= int(serializer.data.get("quantity"))
                amt = prd.cost*int(serializer.data.get("quantity"))
                if dep.hundreds*100 >= amt:
                    h_units = 1
                    while h_units*100 < amt:
                        h_units += 1
                    dep.hundreds -= h_units
                    rem = h_units*100 - amt
                    dep.fifties += rem//50
                    rem = rem%50
                    dep.twenties += rem//20
                    rem = rem%20
                    dep.tens += rem//10
                    rem = rem%10
                    dep.fives += rem//5

                elif dep.fifties*50 >= amt:
                    f_units = 1
                    while f_units*50 < amt:
                        f_units += 1
                    dep.fifties -= f_units
                    rem = f_units*50 - amt
                    dep.twenties += rem//20
                    rem = rem%20
                    dep.tens += rem//10
                    rem = rem%10
                    dep.fives += rem//5

                elif dep.twenties*20 >=amt:
                    tw_units = 1
                    while tw_units*50 < amt:
                        tw_units += 1
                    dep.twenties -= tw_units
                    rem = tw_units*20 - amt
                    dep.tens += rem//10
                    rem = rem%10
                    dep.fives += rem//5

                elif dep.tens*10 >=amt:
                    t_units = 1
                    while t_units*10 < amt:
                        t_units += 1
                    dep.tens -= t_units
                    rem = t_units*10 - amt
                    dep.fives += rem//5

                elif dep.fives*5 >=amt:
                    fi_unit = 1
                    while fi_unit*10 < amt:
                        fi_unit += 1
                    dep.fives -= fi_unit
                dep.total = dep.fives*5 + dep.tens*10 + dep.twenties*20 + dep.fifties*50 + dep.hundreds*100
                status_code = status.HTTP_202_ACCEPTED
                deposit = {
                    'fives': dep.fives,
                    'tens': dep.tens,
                    'twenties': dep.twenties,
                    'fifties': dep.fifties,
                    'hundreds': dep.hundreds
                }
                data = {
                    'productName': prd.productName,
                    'total_cost': amt,
                    'quantity': serializer.data.get("quantity"),
                    'deposit': deposit
                }
                response = {
                    'success': 'True',
                    'status code': status_code,
                    'message': 'Product Purchased Successfully',
                    'data': data
                }
                prd.save()
                dep.save()
                return JsonResponse(response, status=status_code)
        except (ValidationError, ValueError, TypeError, IntegrityError) as msg:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'False',
                'status code': status_code,
                'message': str(msg),
            }
            return JsonResponse(response, status=status_code)

















