from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='user_profile', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics')
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'User Info'

    def __str__(self):
        return self.user.get_full_name()
