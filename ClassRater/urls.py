"""ClassRater URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from homepage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('courses/', views.courses, name='courses'),
    path('reviews/', views.reviews, name='reviews'),
    path('course/<int:id>/', views.course, name='course'),
    path('add_review/<course_id>', views.add_review, name='add_review'),
    path('add_review_search/', views.add_review_search, name='add_review_search'),
    path('users/sign_up/', views.sign_up, name='sign_up'),
    path('users/sign_in/', views.sign_in, name='sign_in'),
    path('users/sign_out/', views.sign_out, name='sign_out'),
    path('course/<course_id>/follow_course_action', views.follow_course_action, name='follow_course_action'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
