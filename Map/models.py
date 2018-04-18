from django.db import models



class Location(models.Model) :
    name = models.CharField(max_length=100, default=None, null=True)
    x_cen = models.FloatField(default=0, null=True, blank=True)
    y_cen = models.FloatField(default=0, null=True, blank=True)

    class Meta :
        unique_together = ("name",)



class Coor(models.Model) :
    x1 = models.FloatField(default=None)
    y1 = models.FloatField(default=None)
    x2 = models.FloatField(default=None)
    y2 = models.FloatField(default=None)
    x_cen = models.FloatField(default=None)
    y_cen = models.FloatField(default=None)
    r = models.FloatField(default=None)     # Averaged radius
    location_parent = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta :
        ordering = ["x_cen", "y_cen", "r"]

    def auto_cal(self) :
        self.x_cen = round((self.x1 + self.x2) / 2., 10)
        self.y_cen = round((self.y1 + self.y2) / 2., 10)
        self.r = round((abs(self.x1 - self.x2) + abs(self.y1 - self.y2)) / 2., 10)

    def dist(self, point) :
        """
        :param point: [tuple of float] 
        :return: float
        """

        d = ((point[0] - self.x_cen) ** 2 + (point[1] - self.y_cen) ** 2 )
        return d

    def is_in(self, x, y) :
        if self.x2 >= x >= self.x1 and self.y1 >= y >= self.y2 :
            return True
        else :
            return False



class Event(models.Model) :
    title = models.CharField(max_length=100, default=None)
    num_like = models.IntegerField(default=0)
    num_dislike = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now=True)
    location_parent = models.ForeignKey(Location, on_delete=models.CASCADE)


    class Meta :
        app_label = "Map"


    def todict(self) :
        event_dict = self.__dict__
        output_dict = dict()
        fields = ["title", "num_like", "num_dislike", "time"]

        for field in fields :
            output_dict[field] = event_dict[field]
        output_dict["time"] = output_dict["time"].strftime("%Y-%m-%d %H:%M:%S")

        return output_dict


    def recount(self) :
        self.num_like = len(self.likes.all())
        self.num_dislike = len(self.dislikes.all())
        self.save()