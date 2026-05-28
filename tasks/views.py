from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Task, Submission, Grade, Comment
from .serializers import TaskSerializer, SubmissionSerializer, SubmissionDetailSerializer, GradeSerializer, CommentSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher():
            return Task.objects.filter(created_by=user)
        return Task.objects.filter(subject__students=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubmissionDetailSerializer
        return SubmissionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher():
            return Submission.objects.filter(task__created_by=user)
        return Submission.objects.filter(student=user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        submission, created = Submission.objects.get_or_create(
            task=task,
            student=request.user,
            defaults={'file': request.FILES.get('file')}
        )

        if not created:
            submission.file = request.FILES.get('file', submission.file)

        submission.status = 'submitted'
        submission.save()
        return Response(SubmissionSerializer(submission).data)

    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        submission = self.get_object()
        score = request.data.get('score')
        feedback = request.data.get('feedback', '')

        grade, created = Grade.objects.get_or_create(
            submission=submission,
            defaults={'score': score, 'feedback': feedback, 'graded_by': request.user}
        )

        if not created:
            grade.score = score
            grade.feedback = feedback
            grade.graded_by = request.user

        grade.save()
        return Response(GradeSerializer(grade).data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(submission__student=self.request.user) | Comment.objects.filter(submission__task__created_by=self.request.user)

    def perform_create(self, serializer):
        submission_id = self.request.data.get('submission')
        serializer.save(author=self.request.user, submission_id=submission_id)
