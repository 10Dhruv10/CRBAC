from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Project

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'semester']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'video']