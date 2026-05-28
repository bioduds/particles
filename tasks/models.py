from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from classes.models import Subject

class Task(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='tasks/', blank=True, null=True)
    due_date = models.DateTimeField()
    max_score = models.FloatField(default=10.0, validators=[MinValueValidator(0)])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.title} - {self.subject.name}"


class Submission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('submitted', 'Entregue'),
        ('graded', 'Avaliada'),
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-submission_date']
        unique_together = ('task', 'student')

    def __str__(self):
        return f"{self.task.title} - {self.student.get_full_name() or self.student.username}"


class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='grades_given')
    graded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return f"{self.submission} - Nota: {self.score}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.submission.status = 'graded'
        self.submission.save()


class Comment(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

    def __str__(self):
        return f"Comentário de {self.author} em {self.submission}"
