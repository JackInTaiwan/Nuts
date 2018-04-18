from django.db import models



""" Parameters """
CHAR_MAX = 100



""" Classes """
class Region(models.Model) :
    name = models.CharField(max_length=CHAR_MAX, default=None)

    def todict(self) :
        output = dict()
        restaurants = []
        for res in self.restaurant_set.all() :
            restaurants.append(res.name)
        output["region"] = self.name
        output["restaurants"] = restaurants

        return output

class Restaurant(models.Model) :
    name = models.CharField(max_length=CHAR_MAX, default=None)
    region_parent = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta :
        ordering = ["region_parent"]