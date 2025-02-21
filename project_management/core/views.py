from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Faculty, Student, Project
from .forms import StudentRegistrationForm, ProjectForm
from django.contrib.auth.models import Group

def home(request):
    return render(request, 'core/home.html')


@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, "You don't have student permissions.")
        return redirect('home')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = request.user.student
            project.save()
            messages.success(request, "Project added successfully!")
            return redirect('dashboard')
    else:
        form = ProjectForm()
    
    projects = Project.objects.filter(student=request.user.student)
    return render(request, 'core/student_dashboard.html', {
        'form': form,
        'projects': projects
    })
    

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Faculty, Student, Project
from .forms import StudentRegistrationForm, ProjectForm

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

@login_required
def faculty_dashboard(request):
    if not hasattr(request.user, 'faculty'):
        messages.error(request, "You don't have faculty permissions.")
        return redirect('home')
    
    faculty = request.user.faculty
    students = Student.objects.filter(faculty=faculty)
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            # Create user with a random password
            import uuid
            temp_password = str(uuid.uuid4())[:8]
            user = User.objects.create_user(
                username=email,
                email=email,
                password=temp_password,
                first_name=first_name,
                last_name=last_name
            )
            
            student = form.save(commit=False)
            student.user = user
            student.faculty = faculty
            student.save()
            
            messages.success(
                request, 
                f"Student {first_name} {last_name} has been added successfully! "
                f"Their temporary password is: {temp_password}"
            )
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    
    context = {
        'form': form,
        'students': students,
        'faculty': faculty,
        'user_full_name': f"{request.user.first_name} {request.user.last_name}",
        'department': faculty.department
    }
    return render(request, 'core/faculty_dashboard.html', context)