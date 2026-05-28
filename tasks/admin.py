from django.contrib import admin
from .models import Task, Submission, Grade, Comment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'due_date', 'max_score', 'created_by')
    list_filter = ('subject', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'status', 'submission_date')
    list_filter = ('status', 'submission_date', 'task')
    search_fields = ('task__title', 'student__username')
    readonly_fields = ('submission_date', 'updated_at')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('submission', 'score', 'graded_by', 'graded_at')
    list_filter = ('score', 'graded_by', 'graded_at')
    search_fields = ('submission__task__title', 'submission__student__username')
    readonly_fields = ('graded_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'submission', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('text', 'author__username', 'submission__task__title')
    readonly_fields = ('created_at', 'updated_at')
