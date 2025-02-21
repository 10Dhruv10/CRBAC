from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.contrib.auth.models import User

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
        return f"Project by {self.student.user.username}"

# Add this signal to automatically set up faculty permissions
@receiver(post_save, sender=Faculty)
def create_faculty_permissions(sender, instance, created, **kwargs):
    if created:
        # Create or get faculty group
        faculty_group, created = Group.objects.get_or_create(name='Faculty')
        
        # Add user to faculty group
        instance.user.groups.add(faculty_group)
        
        # Make sure the user is active
        if not instance.user.is_active:
            instance.user.is_active = True
            instance.user.save()
            
