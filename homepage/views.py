from django.shortcuts import render


def app_layout(request):
    return render(request, 'homepage/app_layout.html')


def landing(request):
    return render(request, 'homepage/landing/landing.html')


def courses(request):
    return render(request, 'homepage/courses/courses.html')


def reviews(request):
    return render(request, 'homepage/reviews/reviews.html')


def add_review(request):
    return render(request, 'homepage/add_review.html')
