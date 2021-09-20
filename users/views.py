from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import BuyerOnly
from users.serializers import UserRegistrationSerializer, UserPwdChangeSerializer,\
    UserDeleteSerializer, DepositSerializer
from .models import Deposit
from django.contrib.auth import get_user_model


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'User registered successfully',
            }

            return JsonResponse(response, status=status_code)
        except (ValidationError, ValueError, TypeError) as msg:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'False',
                'status code': status_code,
                'message': str(msg),
            }
            return JsonResponse(response, status=status_code)


class UserView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = get_user_model().objects.get(username=request.user)
            status_code = status.HTTP_202_ACCEPTED
            if user.role == 'B':
                dep = Deposit.objects.get(buyerId=user)
                data = [{
                    'username': user.username,
                    'role': user.role,
                    'deposit': {
                        'fives': dep.fives,
                        'tens': dep.tens,
                        'twenties': dep.twenties,
                        'fifties': dep.fifties,
                        'hundreds': dep.hundreds,
                        'total': dep.total
                    }
                }]
            elif user.role == 'S':
                data = [{
                    'username': user.username,
                    'role': user.role,
                }]
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': data
            }
            return JsonResponse(response, status=status_code)
        except (ValidationError, ValueError, TypeError) as msg:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'False',
                'status code': status_code,
                'message': str(msg),
            }
            return JsonResponse(response, status=status_code)


class UserChangePwd(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPwdChangeSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid()
            if not self.object.check_password(serializer.data.get("old_password")):
                response = {
                    'success': 'False',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Wrong Old Password',
                }
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
            elif serializer.data.get("new_password") == serializer.data.get("old_password"):
                response = {
                    'success': 'False',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'New Passowrd and Old Passowrd cannot be same',
                }
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
            elif serializer.data.get("new_password") != serializer.data.get("confirm_password"):
                response = {
                    'success': 'False',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'New Password and Confirm Password did not match',
                }
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'success': 'True',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
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


class UserDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDeleteSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid()
            user = get_user_model().objects.get(username=request.user)

            usr = user.username
            user.delete()
            response = {
                'success': 'True',
                'code': status.HTTP_200_OK,
                'message': 'User ' + usr + ' Deleted successfully',
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


class UserDepositView(UpdateAPIView):
    permission_classes = (IsAuthenticated, BuyerOnly,)
    serializer_class = DepositSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid()
            denom = {
                     5: 'fives',
                     10: 'tens',
                     20: 'twenties',
                     50: 'fifties',
                    100: 'hundreds'
                     }
            if int(serializer.data.get("amount")) in denom:
                user = get_user_model().objects.get(username=request.user)
                usr = user.username
                amt = serializer.data.get("amount")
                status_code = status.HTTP_202_ACCEPTED
                dep = Deposit.objects.get(buyerId=user)
                initial = getattr(dep, denom[amt])
                setattr(dep, denom[amt], initial + 1)
                dep.total += amt
                dep.save()
                response = {
                    'success': 'True',
                    'code': status.HTTP_200_OK,
                    'message': 'Amount ' + str(amt) + ' for ' + usr + ' Deposited successfully',
                }
                return JsonResponse(response, status=status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': 'False',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Amount Denomination not valid',
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


class UserDepResetView(UpdateAPIView):
    permission_classes = (IsAuthenticated, BuyerOnly)

    def get_object(self, queryset=None):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            user = get_user_model().objects.get(username=request.user)
            usr = user.username
            status_code = status.HTTP_202_ACCEPTED
            dep = Deposit.objects.get(buyerId=user)
            dep.tens = 0
            dep.fives = 0
            dep.twenties = 0
            dep.fifties = 0
            dep.hundreds = 0
            dep.total = 0
            dep.save()
            response = {
                'success': 'True',
                'code': status.HTTP_200_OK,
                'message': 'Amount reset for ' + usr + ' successfully',
            }
            return JsonResponse(response, status=status_code)
        except (ValidationError, ValueError, TypeError) as msg:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'False',
                'status code': status_code,
                'message': str(msg),
            }
            return JsonResponse(response, status=status_code)


