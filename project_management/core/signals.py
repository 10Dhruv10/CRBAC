from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student
from django.contrib.auth.models import Group

@receiver(post_save, sender=Student)
def create_student_group(sender, instance, created, **kwargs):
    if created:
        student_group, _ = Group.objects.get_or_create(name='Student')
        instance.user.groups.add(student_group)