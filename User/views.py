import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User



@csrf_exempt
def add_user(request) :
    if request.method == "POST" :
        data = json.loads(request.body.decode())
        user_id = data["user_id"]
        user = User(user_id=user_id)
        try :
            user.save()
            return HttpResponse("Succeed")
        except :
            return HttpResponse("User_id has been used")

    else :
        return HttpResponse("Fail")



@csrf_exempt
def vote_weather(request) :
    if request.method == "POST" :
        body = json.loads(request.body.decode())
        user_id = body["user_id"]
        weather = body["weather"]
        try :
            user = User.objects.get(user_id=user_id)
            # user updating the weather column
            user.update_weather(weather)

            return HttpResponse("Succeed")

        except :
            return HttpResponse("Fail")



@csrf_exempt
def dump_users(request) :
    if request.method == "GET" :
        users = User.objects.all()

        return HttpResponse("Succeed")
