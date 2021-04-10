from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from homepage.models import Course
        from homepage.models import Prerequisites

        test_data_course = [
            (10231, 'UnFogging the Future', 1, 4, 'Currently Unavailable', 3.25, 1.5, 12, 12),
            (10221, 'Grammatica in Arithmancy', 0, 3, 'Currently Unavailable', 4.25, 4.5, 10, 9),
            (10111, 'Resonance in Runes and Signs', 1, 3, 'Currently Unavailable', 2.25, 2.0, 13, 13),
            (12357, 'Numerology', 0, 5, 'Currently Unavailable', 3.5, 2.5, 7, 3),
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
