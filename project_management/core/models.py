from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name_plural = "Faculties"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.roll_number}"

class Project(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(upload_to='project_videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.student.user.first_name}"