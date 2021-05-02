from django import forms
from django.forms import ModelForm
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['course', 'user', 'rate', 'content', 'course_load', 'professor']
        CHOICES = [['', '---'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']]
        widgets = {
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
