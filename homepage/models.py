from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True,
                                    validators=[MinValueValidator(0)])  # course id number as given by college
    name = models.CharField(max_length=100)  # course name as given by college
    mandatory = models.BooleanField()  # is the course mandatory (True) or an elective (False)
    credit_points = models.SmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(20)])  # the credit points assigned to this course by the college
    syllabi = models.CharField(max_length=200)  # link to syllabi of the course, not for use, currently
    avg_load = models.DecimalField(max_digits=6, decimal_places=5,
                                   validators=[MinValueValidator(1), MaxValueValidator(5)])  # average course load
    avg_rating = models.DecimalField(max_digits=6, decimal_places=5,
                                     validators=[MinValueValidator(1), MaxValueValidator(5)])  # average course rating
    num_of_raters = models.IntegerField(
        validators=[MinValueValidator(0)])  # number of raters for course rating and course load
    num_of_reviewers = models.IntegerField(
        validators=[MinValueValidator(0)])  # number of reviewers

    def __str__(self):
        return self.name

    def print_details(self):
        mandatory = 'yes' if self.mandatory else 'no'
        msg = (
            "------------------------------------------------------------\n"
            f"Course indentifier: {self.course_id}   \nName: {self.name}\nMandatory? {mandatory}\n"
            f"Credit Points: {self.credit_points}\nSyllabi: {self.syllabi}\n"
            f"Average Rating: {round(self.avg_rating, 3)} \tAverage Load: {round(self.avg_load, 3)}\t"
            f"{self.num_of_raters} Raters\nNumber Of Reviews: {self.num_of_reviewers}"
            )
        print(msg)

    def get_details(self):
        return (self.course_id, self.name, self.mandatory, self.credit_points, self.syllabi,
                self.avg_load, self.avg_rating, self.num_of_raters, self.num_of_reviewers)

    # --- returns all Course objects - the main 'courses' source for the view
    @staticmethod
    def get_courses():
        return Course.objects.all()

    # --- get filtered course list by rating/load/mandatory/elective  - return QuerySets
    @staticmethod
    def get_filtered_courses_by_rating(rating, courses):
        # gets all courses with average rating >= rating
        return courses.filter(avg_rating__gte=rating)

    @staticmethod
    def get_filtered_courses_by_load(load, courses):
        # gets all courses with average course load <= load
        return courses.filter(avg_load__lte=load)

    @staticmethod
    def get_mandatory_courses(courses):
        # gets all courses that are mandatory
        return courses.filter(mandatory=True)

    @staticmethod
    def get_elective_courses(courses):
        # gets all courses that are electives
        return courses.filter(mandatory=False)

    # --- returns if course has Prerequisites
    def has_preqs(self):
        return Prerequisites.does_course_have_prerequisites(self)


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
        return f'Req. Course = {self.req_course_id}, Desired Course = {self.course_id}, Req. Code = {self.req_code}'

    @staticmethod
    def get_prerequisites_for_course(course):
        return Prerequisites.objects.filter(course_id=course)

    @staticmethod
    def does_course_have_prerequisites(course):
        return Prerequisites.get_prerequisites_for_course(course).exists()


class AppUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


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

    @staticmethod  # returns a list of Course objects
    def get_courses_by_professor(professor):
        pro_to_course_list = Professor_to_Course.objects.filter(professor_id=professor)
        return [arg.course_id for arg in pro_to_course_list]

    @staticmethod  # returns a list of Professor objects
    def get_professors_by_course(course):
        pro_to_course_list = Professor_to_Course.objects.filter(course_id=course)
        return [arg.professor_id for arg in pro_to_course_list]

    def __str__(self):
        return f'professor = {self.professor_id.name}, course_id = {self.course_id.course_id}'


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    rate = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField(null=True, blank=True)
    course_load = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    likes_num = models.SmallIntegerField(default=0)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        MAX_WORDS_PREVIEW = 5
        MAX_LENGTH_PREVIEW = 40

        shortened_review = ' '.join(self.content.split()[:MAX_WORDS_PREVIEW])
        shortened_review = shortened_review[:MAX_LENGTH_PREVIEW]

        return f'Shortened review: {shortened_review}...'

    def print_details(self):
        message = (
            f"Course: {self.course}\n"
            f"User: {self.user}\n"
            f"Rating: {self.rate}\n"
            f"{str(self)}\n"    # shortened review content
            f"Course load: {self.course_load}\n"
            f"Likes number: {self.likes_num}\n"
            f"Professor: {self.professor if self.professor else 'N/A'}"
        )

        print(message)

    @classmethod
    def main_feed(cls):
        return cls.objects.order_by('-date')
