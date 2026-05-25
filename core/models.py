from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class TaskStatus(models.Model):
    """
    Status personalizável de tarefa. Cada usuário tem seus próprios status.
    """
    name = models.CharField(max_length=50, verbose_name="Nome do Status")
    color = models.CharField(max_length=7, default='#7aa2f7', verbose_name="Cor (HEX)")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_statuses')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
        ordering = ['order', 'id']
        unique_together = ('name', 'user')


class Task(models.Model):
    ORIGIN_CHOICES = [
        ('Manual', 'Manual'),
        ('GitHub', 'GitHub'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descrição")
    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Status",
        related_name='tasks'
    )
    origin = models.CharField(max_length=20, choices=ORIGIN_CHOICES, default='Manual', verbose_name="Origem")
    external_url = models.URLField(blank=True, null=True, verbose_name="URL Externa (GitHub)")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Data de Entrega")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ['-created_at']


# --- Signals ---

DEFAULT_STATUSES = [
    ('Pendente',     '#f7768e', 0),
    ('Em Andamento', '#ff9e64', 1),
    ('Em Revisão',   '#7dcfff', 2),
    ('Concluída',    '#9ece6a', 3),
]


@receiver(post_save, sender=User)
def create_default_statuses(sender, instance, created, **kwargs):
    """Cria os status padrões automaticamente quando um novo usuário é registrado."""
    if created:
        for name, color, order in DEFAULT_STATUSES:
            TaskStatus.objects.get_or_create(
                name=name,
                user=instance,
                defaults={'color': color, 'order': order}
            )
