from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
        ('homepage', '0002_user_test_data'),
        ('homepage', '0003_course_test_data'),
        ('homepage', '0004_professor_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from homepage.models import AppUser
        from homepage.models import Course
        from homepage.models import Review
        from django.utils import timezone

        users = AppUser.objects.all()
        courses = Course.objects.all()

        test_data_review = [
            (1, courses[0].course_id, users[0].user_id, 5, timezone.now(), "Great course", 3),
            (2, courses[0].course_id, users[0].user_id, 4, timezone.now(), "I've learned a lot!", 2),
            (3, courses[1].course_id, users[1].user_id, 4, timezone.now(), "The course was difficult", 5),
            (4, courses[1].course_id, users[1].user_id, 3, timezone.now(), "I didn't learn anything new", 3),
            (5, courses[2].course_id, users[2].user_id, 4, timezone.now(), "This course helped me to find a job", 2),
            (6, courses[2].course_id, users[2].user_id, 3, timezone.now(), "I didn't understand the material ", 4),
        ]

        with transaction.atomic():
            for tdr in test_data_review:
                Review(*tdr).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
