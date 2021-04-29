import pytest


@pytest.mark.parametrize("valid_route, expected_response", [
    ('', 200),
    ('/courses/', 200),
    ('/reviews/', 200),
    ('/add_review/', 200)
])
def test_valid_routes(client, valid_route, expected_response):
    response = client.get(valid_route)
    assert response.status_code == expected_response


@pytest.mark.parametrize("invalid_route, expected_response", [
    ('courses/', 404),  # missing backslash at the begining
    ('/pic_a_trip', 404),
    ('/shlifim_url/', 404)
])
def test_invalid_routes(client, invalid_route, expected_response):
    response = client.get(invalid_route)
    assert response.status_code == expected_response
