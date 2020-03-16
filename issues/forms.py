from django import forms
from .models import Issue


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ['title',
                  'details',
                  'priority',
                  'owner',
                  'users',
                  'estimated_work_hours',
                  ]
        labels = {
            'users': 'Observers'
        }
        widgets = {
            'users': forms.CheckboxSelectMultiple(),
        }
