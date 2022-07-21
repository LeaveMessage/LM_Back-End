from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import logout, login


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = AccountAuthBackend.authenticate(email=data['email'], password=data['password'])

        if not user:
            return Response({'error': 'Invalid credentials'}, status=HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        user.save()
        login(request, user)
        return Response({'token': token.key}, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def check_login(request):
    if request.method == 'GET':
        header = request.META['HTTP_AUTHORIZATION'][6:]
        user = User.objects.get(token=header)

        if not user:
            return Response({'is_login': 'false'}, status=HTTP_404_NOT_FOUND)

        return Response({'is_login': 'true'}, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')


class AccountAuthBackend(object):
    @staticmethod
    def authenticate(email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.password == password:
                return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user(id_):
        try:
            return User.objects.get(pk=id_) # <-- tried to get by email here
        except User.DoesNotExist:
            return None