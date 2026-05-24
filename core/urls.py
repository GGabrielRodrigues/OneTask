from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard principal (onde ficará a listagem e o relatório)
    path('', views.dashboard, name='dashboard'),
    
    # CRUD Manual
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:id>/update/', views.task_update, name='task_update'),
    path('task/<int:id>/delete/', views.task_delete, name='task_delete'),
    
    # API Importação GitHub
    path('api/task/import/', views.api_task_import, name='api_task_import'),
]
