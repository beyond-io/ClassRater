from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    def generate_user_test_data(apps, schema_editor):
        from homepage.models import User

        users_test_data = [
            ('testUser1', 'user1@gmail.com', 'password123'),
            ("testUser2", "David@gmail.com", "Password456"),
            ("testUser3", "User3@gmail.com", "User3Password")
        ]

        with transaction.atomic():
            for user_name, user_email, user_password in users_test_data:
                User(name=user_name, password=user_password, email=user_email).save()

    operations = [
        migrations.RunPython(generate_user_test_data),
    ]
