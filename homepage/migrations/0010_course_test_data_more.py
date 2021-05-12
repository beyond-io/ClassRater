from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_user_test_data'),
        ('homepage', '0009_alter_course_fields_add_validation'),
    ]

    def generate_data(apps, schema_editor):
        from homepage.models import Course
        from homepage.models import Prerequisites

        test_data_course = [
            (10340, 'No Return - through the Lense', True, 4, None),
            (10341, 'Open Source 101', False, 3, "https://www.github.com", 4.25, 4.5, 10, 9),
            (10342, 'Normalized Spatial Schemes', True, 3, None, 3, 5, 1, 0),
            (12343, 'Easier than Zoology', False, 5, None, 3.5, 2.5, 7, 3),
        ]

        courses = [Course(*tdc) for tdc in test_data_course]
        test_data_prerequisites = [
            (courses[3], courses[0], 1),
            (courses[2], courses[1], 0),
            ]

        with transaction.atomic():
            for course in courses:
                course.save()

            for preq in test_data_prerequisites:
                Prerequisites(course_id=preq[0], req_course_id=preq[1], req_code=preq[2]).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
