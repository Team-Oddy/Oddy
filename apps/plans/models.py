# models.py
from django.db import models

class UserProfile(models.Model):
    nickname = models.CharField(max_length=5)

    def __str__(self):
        return self.nickname

class TravelGroup(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    travel_name = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.travel_name
