from django.db import models
from django.utils import timezone


class Course(models.Model):
    pass


class User(models.Model):
    pass


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.SmallIntegerField()
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    course_load = models.SmallIntegerField()
