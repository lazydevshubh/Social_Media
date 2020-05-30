from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Comment(models.Model):
    content=models.TextField()
    date_created=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:15]


class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_created=models.DateTimeField(default=timezone.now)
    likes=models.ManyToManyField(User,related_name='like')
    comments=models.ManyToManyField(Comment)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        print(reverse('post-details', kwargs={'pk': self.pk}))
        return reverse('post-details', kwargs={'pk': self.pk})