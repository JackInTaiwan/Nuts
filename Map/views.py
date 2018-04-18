import os
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Location, Coor, Event
from User.models import User



@csrf_exempt
def edit_data(request) :
    if request.method == "POST" :
        import pandas as pd
        import numpy as np

        ### Parameters
        DATA_ROOT = os.path.dirname(os.path.dirname(__file__)) + "/data/"   # abs path
        fp = DATA_ROOT + "map.xlsx"

        ### Load data
        data = pd.read_excel(fp)
        data = np.array(data)
        for row in data :
            for i, item in enumerate(row) :
                if i == 0 :
                    loc = Location(name=item)
                    loc.save()
                elif item is not np.nan :
                    if i % 2 == 1 :
                        x1, y1 = float(item.split(", ")[1]), float(item.split(", ")[0])
                        coor = Coor()
                        coor.x1, coor.y1 = x1, y1
                        coor.location_parent = loc
                    else :
                        x2, y2 = float(item.split(", ")[1]), float(item.split(", ")[0])
                        coor.x2, coor.y2 = x2, y2
                        coor.auto_cal()
                        coor.save()
                        if i == 2 :
                            loc.x_cen = coor.x_cen
                            loc.y_cen = coor.y_cen
                            loc.save()
        return HttpResponse("Succeed")

    elif request.method == "DELETE" :
        locations, coors = Location.objects.all(), Coor.objects.all()
        locations.delete()
        coors.delete()

        return HttpResponse("Delete")


@csrf_exempt
def event(request) :
    if request.method == "POST" :
        data = json.loads(request.body.decode())
        coor_x, coor_y = data["coor_x"], data["coor_y"]
        title = data["title"]

        coors = Coor.objects.all()
        for coor in coors :
            if coor.is_in(coor_x, coor_y) :
                loc = coor.location_parent
                event = Event(
                    title=title,
                    location_parent=loc,
                )
                event.save()
                print ("use")
                break

        else : return HttpResponse("Fail")

        return HttpResponse("Succceed")

    elif request.method == "DELETE" :
        data = json.loads(request.body.decode())
        event_id = data["event_id"]
        event = Event.objects.get(id=event_id)
        event.delete()

    else : return HttpResponse("Fail")



@csrf_exempt
def change_comment(request) :
    if request.method == "POST" :
        data = json.loads(request.body.decode())
        user_id = data["user_id"]
        event_id = data["event_id"]
        like = data["like"]
        dislike = data["dislike"]

        if not (like and dislike) :
            user = User.objects.get(user_id=user_id)
            event = Event.objects.get(id=event_id)
            for u in event.likes.all() :
                if u.user_id == user_id :
                    if dislike :
                        event.likes.remove(u)
                        user.likes.remove(event)
                        user.dislikes.add(event)
                    break
            else :
                if like :
                    event.likes.add(user)
                    user.likes.add(event)


            for u in event.dislikes.all() :
                if u.user_id == user_id :
                    if like :
                        event.dislikes.remove(u)
                        user.dislikes.remove(event)
                        user.likes.add(event)
                    break
            else :
                if dislike :
                    event.dislikes.add(user)
                    user.dislikes.add(event)

            event.recount()

        return HttpResponse("Succeed")


@csrf_exempt
def dump_data(request) :
    if request.method == "GET" :
        locations = Location.objects.all()
        output = []
        for location in locations :
            location_data = dict()
            location_data["location"] = location.name
            location_data["x_cen"] = location.x_cen
            location_data["y_cen"] = location.y_cen
            if len(location.event_set.all()) > 0 :
                location_data["events"] = [event.todict() for event in location.event_set.all()]
            else :
                location_data["events"] = []
            output.append(location_data)
        output_json = json.dumps(output)
        return HttpResponse(output_json)

    else :
        return HttpResponse("Fail")



@csrf_exempt
def get_location(request) :
    if request.method == "GET" :
        params = request.GET
        coor_x, coor_y = float(params["coor_x"]), float(params["coor_y"])

        coors = Coor.objects.all()
        loc = None
        for coor in coors :
            if coor.is_in(coor_x, coor_y) :
                loc = coor.location_parent.name
                print ("use")
                break

        if loc != None :
            return HttpResponse(loc)

        else :
            return HttpResponse("None")

    else :
        return HttpResponse("[Fail] Only method GET is allowed")
