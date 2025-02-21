from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import Faculty, Student, Project

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    if hasattr(request.user, 'faculty'):
        return faculty_dashboard(request)
    elif hasattr(request.user, 'student'):
        return student_dashboard(request)
    else:
        messages.error(request, "Account type not recognized.")
        return redirect('home')
def logout_view(request):
    # Remove the comma after logout(request)
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')
@login_required
def faculty_dashboard(request):
    if not hasattr(request.user, 'faculty'):
        messages.error(request, "You don't have faculty permissions.")
        return redirect('home')
    
    faculty = request.user.faculty
    students = Student.objects.filter(faculty=faculty)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return redirect('dashboard')
        
        try:
            # Check if username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('dashboard')
            
            # Create the user account
            user = User.objects.create_user(
                username=username,
                password=password,
                is_active=True  # Ensure the account is active
            )
            
            # Create the student object
            student = Student.objects.create(
                user=user,
                faculty=faculty
            )
            
            # Add to student group
            student_group, _ = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            user.save()
            
            messages.success(request, f"Student account '{username}' created successfully!")
            
        except Exception as e:
            print(f"Error creating student: {str(e)}")  # For debugging
            messages.error(request, "Error creating student account.")
            if user:  # If user was created but student creation failed
                user.delete()  # Clean up the user account
                
        return redirect('dashboard')
    
    return render(request, 'core/faculty_dashboard.html', {
        'students': students
    })

@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, "You don't have student permissions.")
        return redirect('home')
    
    student = request.user.student
    projects = Project.objects.filter(student=student)
    
    if request.method == 'POST':
        description = request.POST.get('description')
        video = request.FILES.get('video')
        
        if description and video:
            Project.objects.create(
                student=student,
                description=description,
                video=video
            )
            messages.success(request, "Project added successfully!")
        else:
            messages.error(request, "Both description and video are required.")
        
        return redirect('dashboard')
    
    return render(request, 'core/student_dashboard.html', {
        'projects': projects
    })