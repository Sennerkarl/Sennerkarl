from django.db import models
from django.db.models.deletion import CASCADE
from django.http import request
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) # get the right time as default
    author = models.ForeignKey(User, on_delete=CASCADE) #relate to User, and set what to do when deleted
    likes = models.ManyToManyField(User, related_name='blog_post')
    picture = models.ImageField(default='worldmap_02.png', upload_to='post_pics')
    

    def __str__(self):
        return self.title

    def get_absolute_url(self): #get a url after creating a post  
        return reverse('post-detail', kwargs={'pk': self.pk}) # reverse will return the url as a string and the post need an extra attribute: the primary key of the post

    def total_likes(self):
        return self.likes.count()
    
    def add_like(self):
        return self.likes.add(self.request.user)

    def remove_like(self):
        return self.likes.remove(self.request.user)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) # get the right time as default
    author = models.ForeignKey(User, on_delete=CASCADE) #relate to User, and set what to do when deleted

    def __str__(self): #define what we see when we print it out
        if len(self.content) < 20:
            return self.content
        else:
            return f'{self.content[0:20]}...'
