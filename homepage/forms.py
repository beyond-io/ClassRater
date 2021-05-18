from django import forms
from django.forms import ModelForm
from .models import Review, Professor_to_Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request')
        user = kwargs.pop('user')
        course = kwargs.pop('course')
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.fields['course'].initial = course
        self.fields['professor'].queryset = Professor_to_Course.get_queryset_professors_by_course(course)

    class Meta:
        model = Review
        fields = ['course', 'user', 'rate', 'content', 'course_load', 'professor']
        CHOICES = [['', '---'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']]
        widgets = {
            'user': forms.HiddenInput(),
            'course': forms.HiddenInput(),
            'rate': forms.Select(choices=CHOICES),
            'course_load': forms.Select(choices=CHOICES),
        }


class FilterForm(forms.Form):
    choices = [('rate_over', 'rating over 3.5'), ('load_below', 'course load under 3.5'),
               ('mand', 'mandatory'), ('elect', 'elective')]
    filter_by = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=choices,
        required=False
        )


# This class uses the built in django UserCreationForm and adds an email field
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User

        # There are 2 password fields to confirm the password (pw1 and pw2 are built-in function names)
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
