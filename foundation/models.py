from django.db import models
import secrets
from .paystack import PayStack
from django.utils import timezone
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

class Blog(models.Model):
    image = models.ImageField(upload_to='blog-img')
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    username = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return self.name

class Event(models.Model):
    image = models.ImageField(upload_to='event-img')
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
class Gallery(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='galary-img', default='')
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
class HomeBlog(models.Model):
    image = models.ImageField(upload_to='homeblog-img')
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
class HomeEvent(models.Model):
    image = models.ImageField(upload_to='homeevent-img')
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
class LatestCause(models.Model):
    image = models.ImageField(upload_to='latestCause-img')
    title = models.CharField(max_length=100)
    value = models.IntegerField()
    amount_raised = models.FloatField()
    amount_goal = models.FloatField()
    
    def __str__(self):
        return self.title
    

class YouTube(models.Model):
    title = models.CharField(max_length=50, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    url = EmbedVideoField()

    class Meta:
        ordering = ['-date_added']
        
    def __str__(self):
        return self.title

class Payment(models.Model):
    amount = models.PositiveBigIntegerField()
    ref = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self) -> str:
        return f"Payment: {self.amount}"
    
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)
    
    def amount_value(self) -> int:
        return self.amount * 101
    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 101 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False