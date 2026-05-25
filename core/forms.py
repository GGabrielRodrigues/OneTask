from django import forms
from .models import Task, TaskStatus


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título da Tarefa'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição detalhada (opcional)'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra os status para mostrar apenas os do usuário logado
        if user:
            self.fields['status'].queryset = TaskStatus.objects.filter(user=user).order_by('order')
        # Data de entrega é sempre opcional
        self.fields['due_date'].required = False
        self.fields['due_date'].label = 'Data de Entrega (opcional)'
        self.fields['status'].label = 'Status'


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = ['name', 'color', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Bloqueado, Em Análise...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control form-control-color',
                'type': 'color',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
        }
        labels = {
            'name': 'Nome do Status',
            'color': 'Cor',
            'order': 'Ordem de exibição',
        }
