from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(default='default.png', upload_to="profile_img",)

    def __str__(self):
        return self.user.username
    
    