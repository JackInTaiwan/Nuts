from django.db import models
from Map.models import Event
from django.utils.timezone import now



class User(models.Model) :
    user_id = models.CharField(max_length=100, blank=False, null=False)
    likes = models.ManyToManyField(Event, related_name="likes")   #
    dislikes = models.ManyToManyField(Event, related_name="dislikes")
    time_create = models.DateTimeField(auto_now_add=True)

    weather = models.CharField(max_length=50, blank=True, null=False)
    # weather has two options: ["sun", "rain"]
    weather_stmp = models.DateTimeField(default=now())

    def __unicode__(self) :
        return self.user_id

    class Meta :
        ordering = ["time_create"]
        unique_together = ["user_id"]

    def update_weather(self, weather) :
        weather_options = ["sun", "rain", "cloud"]
        if weather in weather_options :
            self.weather = weather
            self.weather_stmp = now()
            self.save()
            return True
        else :
            return None