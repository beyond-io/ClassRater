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


class Prerequisites(models.Model):
    # for   course A = the prerequisite course
    #       course B = the course the user wants to take
    # the relatiosnship between them, as depicted by req_code:
    #               -2  if there is no relation between taking course A before or during course B and taking course B
    #               -1  if  course B can't be taken if course A was taken (before or at the same time)
    # req_code =     0  if  course A must be taken at the same time (or before) course B
    #                1  if  course A must be taken before course B

    # choices for the req_code field
    class Req_Code(models.IntegerChoices):
        NONE = -2
        CANT = -1
        SIMU = 0
        BEFORE = 1

    # id of course B
    course_id = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='new_course_id', db_column='course_id')
    # id of course A
    req_course_id = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='required_course_id', db_column='req_course_id')
    # requirement code : depiction of the relationship between A and B as stated above
    req_code = models.SmallIntegerField(choices=Req_Code.choices, default=Req_Code.NONE)


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.SmallIntegerField()
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    course_load = models.SmallIntegerField()


class Professor(models.Model):
    name = models.CharField(max_length=100)


class Professor_to_Course(models.Model):
    professor_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
