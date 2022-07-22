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

from datetime import datetime, timedelta
# Create your views here.
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_post(request):
    data=JSONParser().parse(request)
    if request.method=='POST':
        user = User.objects.get(token=data['token'])
        post_check=Post.objects.filter(user_id=user.id)
        if post_check:
            return Response({'error':'이미 글이 존재합니다.'},status=HTTP_400_BAD_REQUEST)
        Post.objects.create(
            content=data['content'],
            cycle=data['cycle'],
            count=data['count'],
            deadline_date=datetime.today() + timedelta(days=int(data['cycle'])),
            user_id=user
        )
        print(f"deadline_date: {datetime.today() + timedelta(days=int(data['count']))}")
        post=Post.objects.get(user_id=user.id)
        for e in data['reciever']:
            Reciever.objects.create(
                email=e,
                post_id=post    
            )
        return Response({'message':'success'},status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def delete_post(request):
    data=JSONParser().parse(request)
    if request.method=='POST':
        user = User.objects.get(token=data['token'])
        post=Post.objects.get(user_id=user.id)
        post.delete()
        return Response({'message':'success'},status=HTTP_200_OK)

    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_post(request):
    data=JSONParser().parse(request)
    if request.method=='POST':
        user = User.objects.get(token=data['token'])
        post=Post.objects.get(user_id=user.id)
        reciever = Reciever.objects.filter(post_id=post.id)
        recievers=[]
        for r in reciever:
            recievers.append(r.email)
        return Response({'content':post.content,'reciever':f'{recievers}','cycle':post.cycle,'count':post.count},status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_post(request):
    data=JSONParser().parse(request)
    if request.method=='POST':
        user = User.objects.get(token=data['token'])
        post_check=Post.objects.filter(user_id=user.id)
        Post.objects.update(
            content=data['content'],
            cycle=data['cycle'],
            count=data['count'],
            user_id=user
        )
        post=Post.objects.get(user_id=user.id)
        reciever = Reciever.objects.filter(post_id=post.id)
        reciever.delete()
        for e in data['reciever']:
            Reciever.objects.create(
                email=e,
                post_id=post    
            )
        return Response({'message':'success'},status=HTTP_200_OK)


