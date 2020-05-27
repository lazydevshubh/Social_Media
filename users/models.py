from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='./profile_pics/default.jpg',upload_to="profile_pics")

    def __str__(self):
        return str(self.user.username)+" profile"

    def save(self):
        super().save()
        img=Image.open(self.image.path)

        if img.width>300 or img.height>300:
            img.thumbnail((300,300))
            img.save(self.image.path)
