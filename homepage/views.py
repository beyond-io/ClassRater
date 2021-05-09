from django.shortcuts import render, redirect
from homepage.models import Course, Review, AppUser
from homepage.forms import FilterForm, ReviewForm, SignUpForm
from django.contrib.auth import login
from django.contrib import messages


def app_layout(request):
    return render(request, 'homepage/app_layout.html')


def landing(request):
    return render(request, 'homepage/landing/landing.html')


def courses(request):
    all_courses = Course.get_courses()
    filters_active = []
    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            filters = form.cleaned_data.get('filter_by')
            for filter in filters:
                if(filter == 'mand'):
                    all_courses = Course.get_mandatory_courses(all_courses)
                    filters_active.append('mandatory')
                elif(filter == 'elect'):
                    all_courses = Course.get_elective_courses(all_courses)
                    filters_active.append('elective')
                elif(filter == 'load_below'):
                    all_courses = Course.get_filtered_courses_by_load(3.5, all_courses)
                    filters_active.append('course load under 3.5')
                elif(filter == 'rate_over'):
                    all_courses = Course.get_filtered_courses_by_rating(3.5, all_courses)
                    filters_active.append('course rating over 3.5')
    else:
        form = FilterForm()

    context = {'all_courses': all_courses, 'filters': filters_active}
    context['form'] = FilterForm()
    return render(request, 'homepage/courses/courses.html', context)


def reviews(request):
    reviews = Review.main_feed()
    return render(request, 'homepage/reviews/reviews.html', {'reviews': reviews})


def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_review')
    else:
        form = ReviewForm()
    return render(request, 'homepage/add_review.html', {'form': form})


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            appUser = AppUser()
            appUser.user = form.save()
            appUser.save()
            login(request, appUser.user)
            messages.success(request, "Registration successful.")
            return redirect("sign_in")

        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")

    form = SignUpForm
    return render(request=request, template_name="homepage/users/sign_up.html", context={"sign_up_form": form})
