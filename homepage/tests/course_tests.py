import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.parametrize("valid_course_id", [
    (10231), (10111), (10221), (12357)
    ])
@pytest.mark.django_db
def test_renders_course_template(client, valid_course_id):
    response = client.get('/course/' + str(valid_course_id) + '/')

    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/courses/course.html')


@pytest.mark.django_db
def test_invalid_course_resquest(client):
    invalid_id = 11111

    response = client.get('/course/' + str(invalid_id) + '/')
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/courses/courses.html')
