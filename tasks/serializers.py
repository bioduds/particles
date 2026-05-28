from rest_framework import serializers
from .models import Task, Submission, Grade, Comment
from users.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    submissions_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'subject', 'subject_name', 'title', 'description', 'due_date', 'max_score', 'submissions_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_submissions_count(self, obj):
        return obj.submissions.count()

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'author']

class GradeSerializer(serializers.ModelSerializer):
    graded_by_name = serializers.CharField(source='graded_by.get_full_name', read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'submission', 'score', 'feedback', 'graded_by', 'graded_by_name', 'graded_at']
        read_only_fields = ['id', 'graded_at']

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    grade = GradeSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'task', 'task_title', 'student', 'student_name', 'file', 'status', 'grade', 'submission_date']
        read_only_fields = ['id', 'submission_date', 'student', 'status']

class SubmissionDetailSerializer(SubmissionSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(SubmissionSerializer.Meta):
        fields = SubmissionSerializer.Meta.fields + ['comments']
