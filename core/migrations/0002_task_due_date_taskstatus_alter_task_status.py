# Migration com data migration incluída para preservar dados existentes

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


# Mapeamento dos status antigos (texto puro) para nomes e cores padrões
DEFAULT_STATUSES = [
    ('Pendente',     '#f7768e', 0),
    ('Em Andamento', '#ff9e64', 1),
    ('Em Revisão',   '#7dcfff', 2),
    ('Concluída',    '#9ece6a', 3),
]

# Status legados que existiam antes da migração
LEGACY_STATUS_MAP = {
    'Pendente':     'Pendente',
    'Em Andamento': 'Em Andamento',
    'Concluída':    'Concluída',
}


def migrate_tasks_to_fk(apps, schema_editor):
    """
    Data migration: converte os status em texto puro das tasks existentes
    para os novos objetos TaskStatus com FK, atribuindo-os ao campo status_new.
    """
    Task = apps.get_model('core', 'Task')
    TaskStatus = apps.get_model('core', 'TaskStatus')
    User = apps.get_model('auth', 'User')

    for user in User.objects.all():
        user_tasks = Task.objects.filter(user=user)
        if not user_tasks.exists():
            continue

        # Cria os status padrões para este usuário
        for name, color, order in DEFAULT_STATUSES:
            TaskStatus.objects.get_or_create(
                name=name,
                user=user,
                defaults={'color': color, 'order': order}
            )

        # Para cada task, vincula ao status correto usando status_new
        for task in user_tasks:
            old_status_name = task.status  # ainda é string (CharField)
            mapped_name = LEGACY_STATUS_MAP.get(old_status_name, 'Pendente')
            try:
                new_status = TaskStatus.objects.get(name=mapped_name, user=user)
                # Atualiza via queryset para evitar trigger de validação do model
                Task.objects.filter(pk=task.pk).update(status_new=new_status)
            except TaskStatus.DoesNotExist:
                pass



def reverse_migrate(apps, schema_editor):
    """Reversão: não é possível recuperar o texto original de forma precisa."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 1. Adiciona due_date
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de Entrega'),
        ),
        # 2. Cria o model TaskStatus
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome do Status')),
                ('color', models.CharField(default='#7aa2f7', max_length=7, verbose_name='Cor (HEX)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_statuses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
                'ordering': ['order', 'id'],
                'unique_together': {('name', 'user')},
            },
        ),
        # 3. Adiciona temporariamente um campo status_new (FK) com null=True
        migrations.AddField(
            model_name='task',
            name='status_new',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='tasks_new',
                to='core.taskstatus',
                verbose_name='Status',
            ),
        ),
        # 4. Data migration: preenche status_new baseado no status antigo (texto)
        migrations.RunPython(migrate_tasks_to_fk, reverse_migrate),
        # 5. Remove o campo status antigo (CharField)
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
        # 6. Renomeia status_new para status
        migrations.RenameField(
            model_name='task',
            old_name='status_new',
            new_name='status',
        ),
    ]
