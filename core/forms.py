from django import forms
from . models import Year

class CreateProfileForm(forms.Form):
    name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    dni = forms.IntegerField(required=True)
    entry_year = forms.IntegerField(required=True)
    current_year = forms.CharField(required=False)


class CreateTestForm(forms.Form):
    title = forms.CharField(required=True)
    date_day = forms.CharField(required=True)
    date_month = forms.CharField(required=True)
    date_year = forms.CharField(required=True)
    subject = forms.CharField(required=True)


class StudentTestGradeForm(forms.Form):
    grade = forms.IntegerField(required=False)


class CreateTaskForm(forms.Form):
    title = forms.CharField(required=True)
    text = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    date_day = forms.CharField(required=True)
    date_month = forms.CharField(required=True)
    date_year = forms.CharField(required=True)

class StudentTaskGradeForm(forms.Form):
    grade = forms.IntegerField(required=False)
    delivered = forms.CharField(required=True)
