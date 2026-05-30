from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from users.models import User
from classes.models import Subject
from tasks.models import Task, Submission, Comment

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.get_full_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        role = request.POST.get('role', 'student')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role
        )

        messages.success(request, 'Conta criada com sucesso! Faça login.')
        return redirect('login')

    return render(request, 'auth/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado.')
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    context = {}

    if request.user.is_student():
        context['tasks'] = Task.objects.filter(
            subject__students=request.user
        ).order_by('-due_date')
    elif request.user.is_teacher():
        context['subjects'] = Subject.objects.filter(teacher=request.user)
        context['pending_submissions'] = Submission.objects.filter(
            task__created_by=request.user,
            status='submitted'
        ).select_related('task', 'student')

    return render(request, 'tasks/dashboard.html', context)

@login_required(login_url='login')
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.is_student():
        if not task.subject.students.filter(id=request.user.id).exists():
            messages.error(request, 'Você não tem acesso a esta tarefa.')
            return redirect('dashboard')

        if request.method == 'POST':
            file = request.FILES.get('file')
            submission, created = Submission.objects.get_or_create(
                task=task,
                student=request.user
            )
            submission.file = file
            submission.status = 'submitted'
            submission.save()

            messages.success(request, 'Tarefa entregue com sucesso!')
            return redirect('task_detail', task_id=task_id)

    elif request.user.is_teacher():
        if task.created_by != request.user:
            messages.error(request, 'Você não tem acesso a esta tarefa.')
            return redirect('dashboard')

    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required(login_url='login')
@require_http_methods(["POST"])
def comment_create_view(request):
    submission_id = request.POST.get('submission_id')
    text = request.POST.get('text')

    submission = get_object_or_404(Submission, id=submission_id)

    if submission.student != request.user and submission.task.created_by != request.user:
        messages.error(request, 'Você não pode comentar nesta submissão.')
        return redirect('dashboard')

    Comment.objects.create(
        submission=submission,
        author=request.user,
        text=text
    )

    messages.success(request, 'Comentário adicionado!')
    return redirect('task_detail', task_id=submission.task.id)

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'auth/profile.html', {'user': request.user})
