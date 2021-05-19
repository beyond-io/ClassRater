from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
        ('homepage', '0002_user_test_data'),
        ('homepage', '0003_course_test_data'),
        ('homepage', '0006_review_test_data'),
        ('homepage', '0011_user_likes'),
    ]

    def generate_data(apps, schema_editor):
        from homepage.models import User_Likes
        from homepage.models import Review
        from homepage.models import User

        likes_test_data = [
            (User.objects.get(pk=1), Review.objects.get(pk=1)),
            (User.objects.get(pk=1), Review.objects.get(pk=2)),
            (User.objects.get(pk=2), Review.objects.get(pk=3)),
            (User.objects.get(pk=3), Review.objects.get(pk=1)),
        ]

        # testUser1 likes Reviews 1, 2 for course 10111
        # testUser2 likes Review 3 for course 10221
        # testUser3 likes Review 1 for course 10111
        with transaction.atomic():
            for user, review in likes_test_data:
                User_Likes(
                    user_id=user,
                    review_id=review).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
