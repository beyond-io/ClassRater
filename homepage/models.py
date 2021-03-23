from django.db import models
from django.utils import timezone


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)  # course id number as given by college
    name = models.CharField(max_length=100)  # course name as given by college
    mandatory = models.SmallIntegerField()  # is the course mandatory (True) or an elective (False)
    credit_points = models.SmallIntegerField()  # the credit points assigned to this course by the college
    syllabi = models.CharField(max_length=200)  # link to syllabi of the course, not for use, currently
    avg_load = models.DecimalField(max_digits=6, decimal_places=5)  # average course load
    avg_rating = models.DecimalField(max_digits=6, decimal_places=5)  # average course rating
    num_of_raters = models.IntegerField()  # number of raters for course ratnig and course load
    num_of_reviewers = models.IntegerField()  # number of reviewers


class User(models.Model):
    pass


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.SmallIntegerField()
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    course_load = models.SmallIntegerField()
