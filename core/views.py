from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
import os
from django.db.models import Count
from .models import Task, TaskStatus
from .forms import TaskForm, TaskStatusForm


@login_required
def dashboard(request):
    """View principal do OneTask."""
    tasks = Task.objects.filter(user=request.user).select_related('status')
    
    # Contagem dinâmica por status via annotation
    statuses = TaskStatus.objects.filter(user=request.user).annotate(
        task_count=Count('tasks')
    ).order_by('order')

    total_tasks = tasks.count()
    github_pat = os.environ.get('GITHUB_PAT', '')

    context = {
        'tasks': tasks,
        'statuses': statuses,
        'total_tasks': total_tasks,
        'github_pat': github_pat,
        'now': timezone.now(),
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def kanban_board(request):
    """Visão Kanban — tasks agrupadas por status em colunas arrastáveis."""
    statuses = TaskStatus.objects.filter(user=request.user).order_by('order')
    tasks = Task.objects.filter(user=request.user).select_related('status')

    columns = []
    for status in statuses:
        columns.append({
            'status': status,
            'tasks': tasks.filter(status=status),
        })

    context = {
        'columns': columns,
        'now': timezone.now(),
    }
    return render(request, 'core/kanban.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.origin = 'Manual'
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm(user=request.user)

    return render(request, 'core/task_form.html', {'form': form, 'title': 'Nova Tarefa'})


@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(request, 'core/task_form.html', {'form': form, 'title': 'Editar Tarefa'})


@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')

    return render(request, 'core/task_confirm_delete.html', {'task': task})


# --- API Endpoints ---

@login_required
def api_task_import(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description', '')
            external_url = data.get('external_url', '')

            if not title:
                return JsonResponse({'status': 'error', 'message': 'Título é obrigatório.'}, status=400)

            # Pega o primeiro status do usuário (default)
            default_status = TaskStatus.objects.filter(user=request.user).order_by('order').first()

            Task.objects.create(
                title=title,
                description=description,
                status=default_status,
                origin='GitHub',
                external_url=external_url,
                user=request.user
            )
            return JsonResponse({'status': 'success', 'message': 'Tarefa importada com sucesso!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)


@login_required
def api_task_update_status(request, id):
    """Endpoint PATCH para atualizar o status de uma task (drag-and-drop)."""
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=id, user=request.user)
            data = json.loads(request.body)
            status_id = data.get('status_id')

            new_status = get_object_or_404(TaskStatus, id=status_id, user=request.user)
            task.status = new_status
            task.save()

            return JsonResponse({'status': 'success', 'new_status': new_status.name})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)


# --- Status CRUD ---

@login_required
def status_list(request):
    statuses = TaskStatus.objects.filter(user=request.user).order_by('order')
    form = TaskStatusForm()
    return render(request, 'core/status_list.html', {'statuses': statuses, 'form': form})


@login_required
def status_create(request):
    if request.method == 'POST':
        form = TaskStatusForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.user = request.user
            status.save()
    return redirect('status_list')


@login_required
def status_update(request, id):
    status = get_object_or_404(TaskStatus, id=id, user=request.user)
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
    return redirect('status_list')


@login_required
def status_delete(request, id):
    status = get_object_or_404(TaskStatus, id=id, user=request.user)
    if request.method == 'POST':
        # Antes de deletar, desvincula tasks associadas a este status
        Task.objects.filter(user=request.user, status=status).update(status=None)
        status.delete()
    return redirect('status_list')
