from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_user_test_data'),
        ('homepage', '0003_course_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from homepage.models import Course
        from homepage.models import AppUser
        from homepage.models import FollowedUserCourses

        # testUser1 follows Grammatica in Arithmancy
        # testUser2 follows Numerology & UnFogging the Future

        users = AppUser.objects.all()
        followed_courses_test_data = [
            (users[0], Course.objects.get(pk=10221)),
            (users[1], Course.objects.get(pk=12357)),
            (users[1], Course.objects.get(pk=10231))
        ]

        with transaction.atomic():
            for user, course in followed_courses_test_data:
                FollowedUserCourses(user=user, course=course).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
