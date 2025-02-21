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
def dashboard(request):
    try:
        if hasattr(request.user, 'faculty'):
            return faculty_dashboard(request)
        elif hasattr(request.user, 'student'):
            return student_dashboard(request)
        else:
            messages.error(request, "You don't have the required permissions.")
            return redirect('home')
    except:
        messages.error(request, "You don't have the required permissions.")
        return redirect('home')

@login_required
def faculty_dashboard(request):
    if not hasattr(request.user, 'faculty'):
        messages.error(request, "You don't have faculty permissions.")
        return redirect('home')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password="defaultpass123",  # You might want to generate this randomly
                first_name=first_name,
                last_name=last_name
            )
            
            student = form.save(commit=False)
            student.user = user
            student.faculty = request.user.faculty
            student.save()
            
            messages.success(request, f"Student {first_name} {last_name} has been added successfully!")
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    
    students = Student.objects.filter(faculty=request.user.faculty)
    return render(request, 'core/faculty_dashboard.html', {
        'form': form,
        'students': students
    })

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
    

# Add this new logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Modify your dashboard view to properly check faculty permissions
@login_required
def dashboard(request):
    try:
        # Check if user is faculty
        faculty = Faculty.objects.filter(user=request.user).first()
        if faculty:
            return faculty_dashboard(request)
        
        # Check if user is student
        student = Student.objects.filter(user=request.user).first()
        if student:
            return student_dashboard(request)
        
        messages.error(request, "You don't have the required permissions. Please contact admin.")
        return redirect('home')
    except Exception as e:
        messages.error(request, "An error occurred. Please contact admin.")
        return redirect('home')