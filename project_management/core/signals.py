from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Faculty

@receiver(post_save, sender=Faculty)
def setup_faculty_user(sender, instance, created, **kwargs):
    if created:
        # Create or get faculty group
        faculty_group, _ = Group.objects.get_or_create(name='Faculty')
        
        # Add user to faculty group
        instance.user.groups.add(faculty_group)
        
        # Ensure user has a first and last name
        if not instance.user.first_name and not instance.user.last_name:
            instance.user.first_name = instance.user.username
            instance.user.save()