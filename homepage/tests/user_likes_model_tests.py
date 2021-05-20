import pytest
from homepage.models import User, Review, UserLikes, Course


@pytest.fixture
def user_likes_list():
    return list(UserLikes.objects.values_list('user_id', 'review_id'))


@pytest.mark.django_db
def test_user_likes_list(user_likes_list):

    assert user_likes_list == [
        (1, 1),
        (1, 2),
        (2, 3),
        (3, 1)
    ]


@pytest.mark.django_db
def test_add_new_user_like():
    relation = UserLikes(user_id=User.objects.get(pk=3), review_id=Review.objects.get(pk=5))
    relation.save()
    assert UserLikes.objects.filter(pk=relation.id).exists()


@pytest.mark.django_db
def test_like_review():
    user = User.objects.get(pk=2)
    review = Review.objects.get(pk=5)
    likes_num_before = review.likes_num
    UserLikes.toggle_like(user, review)
    assert UserLikes.objects.filter(user_id=user, review_id=review).exists()
    assert review.likes_num == likes_num_before + 1


@pytest.mark.django_db
def test_dislike_review():
    user = User.objects.get(pk=1)
    review = Review.objects.get(pk=1)
    likes_num_before = review.likes_num
    UserLikes.toggle_like(user, review)
    assert not UserLikes.objects.filter(user_id=user, review_id=review).exists()
    assert review.likes_num == likes_num_before - 1


@pytest.mark.django_db
def test_get_reviews_liked_by_user():
    liked_reviews = UserLikes.get_liked_reviews_by_user(User.objects.get(pk=2))
    assert (len(liked_reviews) == 1) and (liked_reviews[0].id == 3)


@pytest.mark.django_db
def test_get_reviews_liked_by_user_for_course():
    liked_reviews = UserLikes.get_liked_reviews_by_user_for_course(
        User.objects.get(pk=2),
        Course.objects.get(pk=10221)
    )
    assert (len(liked_reviews) == 1) and (liked_reviews[0].id == 3)
    assert liked_reviews[0].course_id == 10221


@pytest.mark.django_db
def test_get_users_who_liked_review():
    users = UserLikes.get_users_who_liked_review(Review.objects.get(pk=3))
    assert (len(users) == 1) and users[0].id == 2
