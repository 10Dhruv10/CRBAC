from django.contrib import admin
from .models import Faculty, Student, Project

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'phone')
    search_fields = ('user__first_name', 'user__last_name', 'department')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'roll_number', 'semester')
    list_filter = ('faculty', 'semester')
    search_fields = ('user__first_name', 'user__last_name', 'roll_number')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'created_at', 'updated_at')
    list_filter = ('created_at', 'student__faculty')
    search_fields = ('title', 'description', 'student__user__first_name')