from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import os
from .models import Task
from .forms import TaskForm

@login_required
def dashboard(request):
    """
    View principal do OneTask. 
    Apenas usuários logados podem acessar (@login_required).
    """
    # Buscamos apenas as tarefas do usuário logado
    tasks = Task.objects.filter(user=request.user)
    
    # Cálculos simples para o relatório gerencial
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Concluída').count()
    pending_tasks = tasks.filter(status='Pendente').count()
    in_progress_tasks = tasks.filter(status='Em Andamento').count()
    
    github_pat = os.environ.get('GITHUB_PAT', '')
    
    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'github_pat': github_pat,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.origin = 'Manual'
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    
    return render(request, 'core/task_form.html', {'form': form, 'title': 'Nova Tarefa'})


@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'core/task_form.html', {'form': form, 'title': 'Editar Tarefa'})


@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    
    
    return render(request, 'core/task_confirm_delete.html', {'task': task})


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
            
            # Cria a tarefa baseada nos dados do GitHub
            Task.objects.create(
                title=title,
                description=description,
                status='Pendente',
                origin='GitHub',
                external_url=external_url,
                user=request.user
            )
            return JsonResponse({'status': 'success', 'message': 'Tarefa importada com sucesso!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)

