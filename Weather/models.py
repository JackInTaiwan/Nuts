from django.db import models
from User.models import User
from django.utils.timezone import now



""" Parameters """
reupdate_time = 1   # (minutes)
min_threshold = 1   # the min. of user answering required to update the weather condition



""" Functions """
class Weather(models.Model) :
    sun = models.IntegerField(default=0)
    rain = models.IntegerField(default=0)
    cloud = models.IntegerField(default=0)
    update_stmp = models.DateTimeField(default=now())

    def update(self) :
        if (now() - self.update_stmp).total_seconds() > reupdate_time * 60 :

            users = User.objects.all()
            sun_count, rain_count, cloud_count = 0, 0, 0
            for user in users :
                if (now() - user.weather_stmp).total_seconds() < reupdate_time * 60 :
                    print (user.user_id)
                    if user.weather == "sun" :
                        sun_count += 1
                    elif user.weather == "rain" :
                        rain_count += 1
                    elif user.weather == "cloud" :
                        cloud_count += 1

            self.sun, self.rain, self.cloud = sun_count, rain_count, cloud_count
            self.update_stmp = now()
            self.save()

            return True

        else :
            return False


