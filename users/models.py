from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone


class Message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name="reciever")
    date_sent=models.DateTimeField(default=timezone.now)
    message=models.CharField(max_length=1000)

    def __str__(self):
        return str(self.reciever.username+" "+self.sender.username+" "+self.message)

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

