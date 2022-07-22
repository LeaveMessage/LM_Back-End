from requests import post
from django.core.mail                import EmailMessage
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
from user import random_code

from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Create your views here.
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def check_post(request):
    data=JSONParser().parse(request)
    if request.method=='POST':
        user = User.objects.get(token=data['token'])
        post_check=Post.objects.filter(user_id=user.id)
        if post_check:
            return Response({'error':'이미 글이 존재합니다.'},status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_200_OK)


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
            deadline_date=(datetime.today() + relativedelta(months=int(data['cycle']))),
            user_id=user
        )
        print(f"deadline_date: {datetime.today() + relativedelta(months=int(data['cycle']))}")
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
        if not post_check:
            return Response({'error':'글이 존재하지 않습니다.'},status=HTTP_400_BAD_REQUEST)
        else:
            post_check.delete()
            Post.objects.create(
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


def expiry_check():
    today = datetime.now(timezone('Asia/Seoul'))
    for post in Post.objects.all():
        if post.deadline_date - today:
            code = random_code.make_code()
            message_data = "인증코드: " + code

            mail_title = "남김 life_code 발송"

            user = post.user_id
            mail_to = user.email
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()

            user.lifecode = code
            user.save()


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def send(request):
    data = JSONParser().parse(request)
    if request.method == 'POST':
        user = User.objects.get(token=data['token'])
        post = Post.objects.get(user_id=user.id)
        message_data = post.content
        recievers = Reciever.objects.filter(post_id=post.id)
        print(recievers)
        
        if recievers:
            for reciever in recievers:
                mail_title = f"{user.name}님이 남김."
                mail_to = reciever.email
                email = EmailMessage(mail_title, message_data, to=[mail_to])
                email.send()
            return Response({'message': 'success'}, status=HTTP_200_OK)
        else: return Response({'error':'수신자가 존재하지 않습니다.'},status=HTTP_400_BAD_REQUEST)
    return Response({'error': '뭔가 고장났음.'}, status=HTTP_400_BAD_REQUEST)
        





