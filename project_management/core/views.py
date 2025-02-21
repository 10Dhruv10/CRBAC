from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Faculty, Student, Project
from .forms import ProjectForm
from django.contrib.auth.models import Group

def home(request):
    return render(request, 'core/home.html')


from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Faculty, Student, Project
from .forms import ProjectForm

def logout_view(request):
    # Remove the comma after logout(request)
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')

@login_required
def dashboard(request):
    try:
        # Check if user is faculty
        faculty = Faculty.objects.filter(user=request.user).first()
        if faculty:
            # Add user information to context
            context = {
                'faculty': faculty,
                'user_full_name': f"{request.user.first_name} {request.user.last_name}",
                'department': faculty.department
            }
            return render(request, 'core/faculty_dashboard.html', context)
        
        # Check if user is student
        student = Student.objects.filter(user=request.user).first()
        if student:
            return student_dashboard(request)
        
        messages.error(request, "You don't have the required permissions. Please contact admin.")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')
    
    
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import Faculty, Student, Project

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
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken.")
                return redirect('dashboard')
            
            # Create user with provided username and password
            user = User.objects.create_user(
                username=username,
                password=password,
                is_active=True  # Make sure the user is active
            )
            
            # Create student and link to faculty
            student = Student.objects.create(
                user=user,
                faculty=faculty
            )
            
            # Add user to Student group
            student_group, _ = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            
            messages.success(request, f"Student account created successfully! Username: {username}")
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f"Error creating student: {str(e)}")
            return redirect('dashboard')
    
    context = {
        'students': students,
        'faculty': faculty,
    }
    return render(request, 'core/faculty_dashboard.html', context)

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
            return redirect('dashboard')
        else:
            messages.error(request, "Both description and video are required.")
    
    return render(request, 'core/student_dashboard.html', {'projects': projects})