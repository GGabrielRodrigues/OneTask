from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard principal
    path('', views.dashboard, name='dashboard'),

    # Kanban Board
    path('kanban/', views.kanban_board, name='kanban_board'),

    # CRUD de Tarefas
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:id>/update/', views.task_update, name='task_update'),
    path('task/<int:id>/delete/', views.task_delete, name='task_delete'),

    # CRUD de Status Personalizados
    path('status/', views.status_list, name='status_list'),
    path('status/create/', views.status_create, name='status_create'),
    path('status/<int:id>/update/', views.status_update, name='status_update'),
    path('status/<int:id>/delete/', views.status_delete, name='status_delete'),

    # APIs
    path('api/task/import/', views.api_task_import, name='api_task_import'),
    path('api/task/<int:id>/status/', views.api_task_update_status, name='api_task_update_status'),
]
