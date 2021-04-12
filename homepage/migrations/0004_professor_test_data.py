from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
        ('homepage', '0003_course_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from homepage.models import Course
        from homepage.models import Professor
        from homepage.models import Professor_to_Course

        professor_test_data = [
            ('Septima Vector'),
            ('Sybill Patricia Trelawney'),
            ('Bathsheda Babbling'),
        ]

        professors = [Professor(name=data) for data in professor_test_data]

        # 10221 - Grammatica in Arithmancy, Septima Vector
        # 12357 - Numerology, Septima Vector
        # 10231 - UnFogging the Future, Sybill Patricia Trelawney
        # 10111 - Resonance in Runes and Signs, Bathsheda Babbling
        pro_to_course_test_data = [
            (professors[0], Course.objects.get(pk=10221)),
            (professors[0], Course.objects.get(pk=12357)),
            (professors[1], Course.objects.get(pk=10231)),
            (professors[2], Course.objects.get(pk=10111)),
        ]

        with transaction.atomic():
            for professor in professors:
                professor.save()

            for professor, course_id in pro_to_course_test_data:
                Professor_to_Course(
                    professor_id=professor,
                    course_id=course_id).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
