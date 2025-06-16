# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    class Actions(models.TextChoices):
        todo = 'TODO'
        doing = 'DOING'
        done = 'DONE'
    
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    descricao = models.CharField(max_length=300, verbose_name='Descrição', null=True, blank=True)
    status = models.CharField(max_length=10, default="TODO", choices=Actions.choices)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
