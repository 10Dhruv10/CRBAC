from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('departments/', views.department_selection, name='department_selection'),
    path('departments/<str:department_code>/', views.department_projects, name='department_projects'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]