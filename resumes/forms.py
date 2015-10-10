from django import forms

from resumes.models import Resume


class ResumeFilterForm(forms.Form):
    GRAD_CHOICES = [(name, name) for dt, name in Resume.GRADUATION_CHOICES]

    submitted_by = forms.DateField(required=False)
    graduation = forms.MultipleChoiceField(
        choices=GRAD_CHOICES, required=False,
        widget=forms.CheckboxSelectMultiple()
    )
