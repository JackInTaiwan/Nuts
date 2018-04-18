import os
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Region, Restaurant



@csrf_exempt
def edit_data(request) :
    if request.method == "POST" :
        import pandas as pd
        import numpy as np


        ### Parameters

        DATA_ROOT = os.path.dirname(os.path.dirname(__file__)) + "/data/"   # abs path
        fp = DATA_ROOT + "restaurant.xlsx"
        SHEET_SIZE = 5


        ### Dump data
        sheet_names = pd.ExcelFile(fp).sheet_names

        for i in range(SHEET_SIZE) :
            sheet_data = pd.read_excel(fp, sheet_name=i)
            sheet_data = np.array(sheet_data)
            region = Region(name=sheet_names[i])
            region.save()
            for res in sheet_data[:,0] :
                restaurant = Restaurant(
                    name=res,
                    region_parent=region,
                )
                restaurant.save()
        return HttpResponse("Succeed")

    elif request.method == "DELETE" :
        restaurants = Restaurant.objects.all()
        restaurants.delete()
        return HttpResponse("Delete")

    else :
        return HttpResponse("Fail")


@csrf_exempt
def dump_data(request) :
    if request.method == "GET" :
        output = []
        for region in Region.objects.all() :
            output.append(region.todict())

        output_json = json.dumps(output)
        return HttpResponse(output_json)

    else :
        return HttpResponse("Fail")
