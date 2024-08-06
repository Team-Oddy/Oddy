from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=5, null=True)
    travel_type = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.nickname if self.nickname else self.user.username  # 닉네임이 없으면 카카오톡이름을 반환

class TravelGroup(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='travel_groups')
    travel_name = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()
    invite_code = models.CharField(max_length=6, null=True)

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
