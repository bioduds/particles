from django.db import models
from users.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects_taught')
    students = models.ManyToManyField(User, related_name='subjects_enrolled', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - Prof. {self.teacher.get_full_name() or self.teacher.username}"
