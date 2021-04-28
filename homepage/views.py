from django.shortcuts import render, redirect
from .forms import ReviewForm


def app_layout(request):
    return render(request, 'homepage/app_layout.html')


def landing(request):
    return render(request, 'homepage/landing/landing.html')


def courses(request):
    return render(request, 'homepage/courses/courses.html')


def reviews(request):
    return render(request, 'homepage/reviews/reviews.html')


def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_review')
    else:
        form = ReviewForm()
    return render(request, 'homepage/add_review.html', {'form': form})
