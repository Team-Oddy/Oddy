from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import random
import string

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=5, null=True)
    travel_type = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.nickname if self.nickname else self.user.username

class TravelGroup(models.Model):
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_travel_groups', null=True)
    members = models.ManyToManyField(UserProfile, related_name='joined_travel_groups')
    travel_name = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()
    invite_code = models.CharField(max_length=6, unique=True, null=True)

    def __str__(self):
        return self.travel_name

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)

    def generate_invite_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not TravelGroup.objects.filter(invite_code=code).exists():
                return code

class TravelPlan(models.Model):
    CATEGORY_CHOICES = [
        ('play', 'PLAY'),
        ('eat', 'EAT'),
        ('stay', 'STAY'),
        ('others', 'OTHERS'),
    ]
    
    travel_group = models.ForeignKey(TravelGroup, on_delete=models.CASCADE, related_name='travel_plans')
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_plans')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    place = models.CharField(max_length=200)
    address = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    plan_start_time = models.TimeField(null=True, blank=True)
    plan_end_time = models.TimeField(null=True, blank=True)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.travel_group.travel_name} - {self.category}: {self.place} on {self.date} from {self.plan_start_time} to {self.plan_end_time}"
