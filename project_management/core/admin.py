from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Faculty, Student, Project

class FacultyInline(admin.StackedInline):
    model = Faculty
    can_delete = False
    verbose_name_plural = 'Faculty'

class CustomUserAdmin(UserAdmin):
    inlines = (FacultyInline,)

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'phone')
    search_fields = ('user__first_name', 'user__last_name', 'department')

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new faculty members
            # Make sure the user is active
            obj.user.is_active = True
            obj.user.save()
        super().save_model(request, obj, form, change)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Faculty, Student, Project

class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'get_full_name', 'faculty', 'semester')
    list_filter = ('faculty', 'semester')
    search_fields = ('roll_number', 'user__first_name', 'user__last_name', 'user__email')
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Student Name'

admin.site.register(Student, StudentAdmin)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'created_at', 'updated_at')
    list_filter = ('created_at', 'student__faculty')
    search_fields = ('title', 'description', 'student__user__first_name')