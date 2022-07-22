from requests import post
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.decorators import permission_classes, api_view
import json
from django.http                     import HttpResponse, JsonResponse
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Post
from user.models import User
from reciever.models import Reciever
# Create your views here.
@api_view(['GET','POST','DELETE'])
@permission_classes((AllowAny,))
def crud_post(request):
    data=JSONParser().parse(request)
    if request.method=='POST':
        user = User.objects.get(token=data['token'])
        Post.objects.create(
            content=data['content'],
            cycle=data['cycle'],
            count=data['count'],
            user_id=user
        )
        post=Post.objects.get(user_id=user.id)
        for e in data['reciever']:
            Reciever.objects.create(
                email=e,
                post_id=post      
            )
        return Response({'message':'success'},status=HTTP_200_OK)
    elif request.method=='DELETE':
        print(3)
        return Response({'message':'success'},status=HTTP_200_OK)
    elif request.method=='GET':
        print(2)
        return Response(status=HTTP_200_OK) 

