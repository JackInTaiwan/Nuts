import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Weather



@csrf_exempt
def get_whether(request) :
    if request.method == "GET" :
        try :
            weather = Weather.objects.all()[0]
        except :
            weather = Weather()
            weather.save()

        # update the Weather object
        try :
            weather = Weather.objects.all()[0]
        except :
            weather = Weather()
            weather.save()

        if weather.update() :
            print ("Update Weather Successfully.")
        else :
            print ("Weather is not updated.")

        sun = weather.sun
        rain = weather.rain
        cloud = weather.cloud
        output = dict()
        output["sun"], output["rain"], output["cloud"] = sun, rain, cloud
        output_json = json.dumps(output)

        return HttpResponse(output_json)

    else :
        return HttpResponse("[Fail] Only method GET is allowed.")


