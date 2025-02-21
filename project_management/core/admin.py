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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Faculty, Student, Project

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'faculty', 'get_date_joined')
    list_filter = ('faculty',)
    search_fields = ('user__username',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    
    def get_date_joined(self, obj):
        return obj.user.date_joined
    get_date_joined.short_description = 'Date Joined'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('get_student_username', 'description', 'created_at')
    list_filter = ('student__faculty', 'created_at')
    search_fields = ('student__user__username', 'description')

    def get_student_username(self, obj):
        return obj.student.user.username
    get_student_username.short_description = 'Student'

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'department', 'phone')
    search_fields = ('user__username', 'department')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'