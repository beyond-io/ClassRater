import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_renders_reviews_template(client):
    response = client.get('/reviews/')

    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/reviews/reviews.html')
