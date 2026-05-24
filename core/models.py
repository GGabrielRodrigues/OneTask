from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em Andamento', 'Em Andamento'),
        ('Concluída', 'Concluída'),
    ]

    ORIGIN_CHOICES = [
        ('Manual', 'Manual'),
        ('GitHub', 'GitHub'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descrição")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente', verbose_name="Status")
    origin = models.CharField(max_length=20, choices=ORIGIN_CHOICES, default='Manual', verbose_name="Origem")
    external_url = models.URLField(blank=True, null=True, verbose_name="URL Externa (GitHub)")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ['-created_at']
