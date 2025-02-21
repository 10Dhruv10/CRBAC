from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return self.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.user.username

class Project(models.Model):
    title = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='projects')
    description = models.TextField()
    video = models.FileField(upload_to='project_videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.student.user.username}"
# Signal to ensure student group assignment
@receiver(post_save, sender=Student)
def create_student_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Student')
        instance.user.groups.add(group)
        instance.user.save()

# Signal for faculty group assignment
@receiver(post_save, sender=Faculty)
def create_faculty_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Faculty')
        instance.user.groups.add(group)
        instance.user.save()