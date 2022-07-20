from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# session test
from django.contrib.sessions.models import Session

def index(request):
    try:
        sessionid = request.COOKIES['sessionid']
        s = Session.objects.get(pk=sessionid)
        userid = s.get_decoded()['_auth_user_id']
        print(userid)
    except:
        print(request.COOKIES)
        print('login error!')

    return HttpResponse("Post 페이지가 뜨나요?")
