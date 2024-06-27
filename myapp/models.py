from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.

class MovingPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - Points: {self.points} - {self.timestamp}"

@receiver(post_save, sender=MovingPoints)
def update_total_points(sender, instance, created, **kwargs):
    if created:  # 只在創建新記錄時執行
        TotalPoints.update_total_points(instance.user)
    
class TotalPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.user.username}, Total Points: {self.total_points}"

    @staticmethod
    def update_total_points(user):
        total_points = MovingPoints.objects.filter(user=user).aggregate(total_points=models.Sum('points'))['total_points']
        if total_points is None:
            total_points = 0
        total_points_obj, created = TotalPoints.objects.get_or_create(user=user)
        total_points_obj.total_points = total_points
        total_points_obj.save()