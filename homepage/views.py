from django.shortcuts import render, redirect
from homepage.models import Course, Review, AppUser, UserLikes, User, FollowedUserCourses, Prerequisites
from homepage.forms import FilterAndSortForm, ReviewForm, SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def app_layout(request):
    return render(request, 'homepage/app_layout.html')


def landing(request):
    last_reviews = Review.landing_page_feed()
    return render(request, 'homepage/landing/landing.html', {'reviews': last_reviews})


def courses(request):
    all_courses = Course.get_courses()
    filters_active = []
    sort_active = ''
    if request.method == "GET":
        form = FilterAndSortForm(request.GET)
        if form.is_valid():
            filters = form.cleaned_data.get('filter_by')
            sort_val = form.cleaned_data.get('sort_by')
            sort_result = Course.get_sorted_courses(all_courses, sort_val)
            filter_result = Course.get_filtered_courses(sort_result['result'], filters)
            all_courses = filter_result['result']
            filters_active = filter_result['active']
            sort_active = sort_result['active']
    else:
        form = FilterAndSortForm()

    context = {'all_courses': all_courses, 'filters': filters_active, 'sort': sort_active}
    context['form'] = form
    return render(request, 'homepage/courses/courses.html', context)


def reviews(request):
    reviews = Review.main_feed()
    liked_reviews = []
    if not request.user.is_anonymous:
        liked_reviews = UserLikes.get_liked_reviews_by_user(request.user)
    return render(request, 'homepage/reviews/reviews.html', {'reviews': reviews, 'liked_reviews': liked_reviews})


@login_required(login_url='/users/sign_in/')
def add_review(request, course_id):
    if Review.user_already_posted_review(request.user.id, course_id):
        messages.error(request, 'You have already posted a review for this course')
        return redirect(f'/course/{course_id}/')

    try:
        course = Course.objects.get(pk=course_id)
    except ObjectDoesNotExist:
        return redirect('/add_review_search/')

    if request.method == "POST":
        form = ReviewForm(request.POST, user=request.user.id, course=course_id)
        if form.is_valid():
            review = form.save()
            course = Course.objects.get(pk=review.course.course_id)
            course.update_course_per_review(review.rate, review.course_load, review.content)
            return redirect(f'/course/{course_id}/')
    else:
        form = ReviewForm(user=request.user.id, course=course_id)
    return render(request, 'homepage/add_review.html', {'form': form, 'course_name': course.name})


def course(request, id):
    try:
        course = Course.objects.get(pk=id)
        reviews = Review.objects.filter(course=id).order_by('-likes_num')
        preq = Prerequisites.get_prerequisites_for_course(course)
        liked_reviews = []
        is_following = False
        if not request.user.is_anonymous:
            liked_reviews = UserLikes.get_liked_reviews_by_user_for_course(request.user, course)
            is_following = FollowedUserCourses.is_following_course(request.user, course)
        return render(request, 'homepage/courses/course.html', {
            'id': id,
            'course': course,
            'reviews': reviews,
            'liked_reviews': liked_reviews,
            'is_following': is_following,
            'preq': preq
        })
    except ObjectDoesNotExist:
        return redirect('courses')


@login_required(login_url='/users/sign_in/')
def add_review_search(request):
    if request.method == "GET":
        course_name = request.GET.get('course')
        if not course_name:
            course_name = ''
        courses = Course.get_courses_ordered_by_name(course_name)
        return render(request, 'homepage/add_review_search.html', {'course_name': course_name, 'courses': courses})


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            app_user = AppUser()
            app_user.user = form.save()
            app_user.save()
            login(request, app_user.user)
            messages.success(request, "Registration successful.")
            return redirect("sign_in")

        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")

    form = SignUpForm
    return render(request=request, template_name="homepage/users/sign_up.html", context={"sign_up_form": form})


def sign_in(request):
    sign_in_successful = False

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                sign_in_successful = True
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('landing')

        if not sign_in_successful:
            messages.error(request, 'Invalid username or password.')
            return redirect('sign_in')

    form = AuthenticationForm()
    return render(request=request, template_name='homepage/users/sign_in.html', context={'sign_in_form': form})


def sign_out(request):
    messages.info(request, f'{request.user.username} successfully logged out')
    logout(request)
    return redirect('landing')


def like_review(request, user_id, review_id):
    if request.META.get('HTTP_REFERER') is None:
        return redirect('landing')
    try:
        user = User.objects.get(pk=user_id)
        review = Review.objects.get(pk=review_id)
        UserLikes.toggle_like(user, review)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # stay in referring page
    except ObjectDoesNotExist:
        return redirect('landing')


@login_required(login_url='/users/sign_in/')
def follow_course_action(request, course_id):
    try:
        course = Course.objects.get(course_id=course_id)
    except ObjectDoesNotExist:
        return redirect('/courses/')

    is_following_course = FollowedUserCourses.is_following_course(request.user, course)
    if (is_following_course):
        FollowedUserCourses.unfollow_course(request.user, course)
        messages.success(request, 'Successfully unfollowed this course')
    else:
        FollowedUserCourses.follow_course(request.user, course)
        messages.success(request, 'Successfully followed this course')

    return redirect(f'/course/{course_id}/')


@login_required(login_url='/users/sign_in/')
def my_profile(request):
    try:
        followed_user_courses = FollowedUserCourses.get_courses_followed_by_app_user(request.user.appuser)
        last_user_reviews = Review.profile_page_feed(request.user)
        return render(request, 'homepage/users/my_profile.html', {'user_reviews': last_user_reviews,
                      'user_followed_courses': followed_user_courses})

    except AppUser.DoesNotExist:
        return render(request, 'homepage/users/my_profile.html', {'user_reviews': None,
                      'user_followed_courses': None})
