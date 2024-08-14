from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
import random
import string

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=5, null=True)
    travel_type = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.nickname if self.nickname else self.user.username

class TravelGroup(models.Model):
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_travel_groups', null =True)
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

from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

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
    like_count = models.PositiveIntegerField(default=0)  # 좋아요 수 필드 추가
    comment_count = models.PositiveIntegerField(default=0)  # 댓글 수 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    airplane_text = models.CharField(max_length=50, null=True, blank=True)  # 비행기 텍스트 저장 필드 추가

    def __str__(self):
        return f"{self.travel_group.travel_name} - {self.category}: {self.place} on {self.date} from {self.plan_start_time} to {self.plan_end_time}"

class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    travel_plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'travel_plan')  # 한 유저가 같은 여행 계획에 중복으로 좋아요를 누르지 못하도록 설정

class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    travel_plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname} on {self.travel_plan.place}: {self.content[:20]}"




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# Signal 설정
@receiver(post_save, sender=Like)
def increase_like_count(sender, instance, created, **kwargs):
    if created:
        instance.travel_plan.like_count += 1
        instance.travel_plan.save()

@receiver(post_delete, sender=Like)
def decrease_like_count(sender, instance, **kwargs):
    instance.travel_plan.like_count -= 1
    instance.travel_plan.save()

@receiver(post_save, sender=Comment)
def increase_comment_count(sender, instance, created, **kwargs):
    if created:
        instance.travel_plan.comment_count += 1
        instance.travel_plan.save()

@receiver(post_delete, sender=Comment)
def decrease_comment_count(sender, instance, **kwargs):
    instance.travel_plan.comment_count -= 1
    instance.travel_plan.save()