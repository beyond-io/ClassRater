from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
        ('homepage', '0002_user_test_data'),
        ('homepage', '0003_course_test_data'),
        ('homepage', '0005_professor_test_data')
    ]

    def generate_data(apps, schema_editor):
        from homepage.models import AppUser
        from homepage.models import Course
        from homepage.models import Review
        from homepage.models import Professor
        from django.utils import timezone
        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.conf import settings

        users = AppUser.objects.all()
        courses = Course.objects.all()
        professors = Professor.objects.all()

        image_path = settings.MEDIA_ROOT + '/images/test_image.jpg'
        image = SimpleUploadedFile(
            name='new_test_image.jpg',
            content=open(image_path, 'rb').read(),
            content_type='image/jpeg')

        test_data_review = [
            (1, courses[0].course_id, users[0].user.id, 5, timezone.now(),
                "Great course", 3, 10, professors[2].id, image),
            (2, courses[0].course_id, users[0].user.id, 4, timezone.now(), "I've learned a lot!", 2, 4),
            (3, courses[1].course_id, users[1].user.id, 4.5, timezone.now(),
                "The course was difficult", 5, 0, professors[0].id),
            (4, courses[1].course_id, users[1].user.id, 3.2, timezone.now(), "I didn't learn anything new", 3.7),
            (5, courses[2].course_id, users[2].user.id, 4.5, timezone.now(),
                "This course helped me to find a job", 2.5),
            (6, courses[2].course_id, users[2].user.id, 3.5, timezone.now(), "I didn't understand the material ", 4),
        ]

        with transaction.atomic():
            for tdr in test_data_review:
                Review(*tdr).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
