from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)  # course id number as given by college
    name = models.CharField(max_length=100)  # course name as given by college
    mandatory = models.BooleanField()  # is the course mandatory (True) or an elective (False)
    credit_points = models.SmallIntegerField()  # the credit points assigned to this course by the college
    syllabi = models.CharField(max_length=200)  # link to syllabi of the course, not for use, currently
    avg_load = models.DecimalField(max_digits=6, decimal_places=5)  # average course load
    avg_rating = models.DecimalField(max_digits=6, decimal_places=5)  # average course rating
    num_of_raters = models.IntegerField()  # number of raters for course ratnig and course load
    num_of_reviewers = models.IntegerField()  # number of reviewers

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f'req_cour = {self.req_course_id}, desired_cour = {self.course_id}, req_code = {self.req_code}'


class AppUser(models.Model):
    # This field is the built-in django user model
    # We currently use the following attributes from the django user model: username, password, email, is_active
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

    def toggle_user_activation(self):
        self.user.is_active = not(self.user.is_active)

    @staticmethod
    # Creates a new appUser (without superuser permmisions) and saves it in the DB
    # The is_active attribute of AppUser.user is automaticly set to 'True' when creating a new AppUser
    def create_appUser(username, email, password):
        appUser = AppUser()
        user = User.objects.create_user(username, email, password)
        appUser.user = user

        appUser.save()
        return appUser

    @staticmethod
    def get_all_appUsers():
        return list(AppUser.objects.all())

    @staticmethod
    def find_appUser(username_ToFind):
        try:
            user = User.objects.get(username=username_ToFind)
            return AppUser.objects.get(user=user)
        except:
            return None


class FollowedUserCourses(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'user = {self.user}, course = {self.course}'


class Professor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Professor_to_Course(models.Model):
    professor_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'professor_id = {self.professor_id}, course_id = {self.course_id}'


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    rate = models.SmallIntegerField()
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField(null=True, blank=True)
    course_load = models.SmallIntegerField()
    likes_num = models.SmallIntegerField(default=0)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        MAX_WORDS_PREVIEW = 5
        MAX_LENGTH_PREVIEW = 40

        shortened_review = ' '.join(self.content.split()[:MAX_WORDS_PREVIEW])
        shortened_review = shortened_review[:MAX_LENGTH_PREVIEW]

        return f'Preview: {shortened_review}...'
