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
from .forms import StudentCreationForm

@login_required
def faculty_dashboard(request):
    # Check if user is faculty
    if not hasattr(request.user, 'faculty'):
        messages.error(request, "You don't have faculty permissions.")
        return redirect('home')
    
    faculty = request.user.faculty
    students = Student.objects.filter(faculty=faculty)
    form = StudentCreationForm()  # Initialize the form
    
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                # Check if username exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, "This username is already taken.")
                    return redirect('dashboard')
                
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                
                # Create student profile
                Student.objects.create(
                    user=user,
                    faculty=faculty
                )
                
                # Add to student group
                student_group, _ = Group.objects.get_or_create(name='Student')
                user.groups.add(student_group)
                
                messages.success(request, f"Student account created successfully! Username: {username}")
                return redirect('dashboard')
                
            except Exception as e:
                messages.error(request, f"Error creating student account: {str(e)}")
                return redirect('dashboard')
    
    context = {
        'form': form,
        'students': students,
    }
    
    return render(request, 'core/faculty_dashboard.html', context)

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