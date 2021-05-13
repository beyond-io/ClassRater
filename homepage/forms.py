from django import forms
from django.forms import ModelForm
from .models import Review, Professor_to_Course


class ReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course')
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['course'].initial = course
        self.fields['professor'].queryset = Professor_to_Course.get_queryset_professors_by_course(course)

    class Meta:
        model = Review
        fields = ['course', 'user', 'rate', 'content', 'course_load', 'professor']
        CHOICES = [['', '---'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']]
        widgets = {
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
