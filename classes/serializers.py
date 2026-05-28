from rest_framework import serializers
from .models import Subject
from users.serializers import UserSerializer

class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'teacher', 'teacher_name', 'students_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_students_count(self, obj):
        return obj.students.count()

class SubjectDetailSerializer(SubjectSerializer):
    students = UserSerializer(many=True, read_only=True)

    class Meta(SubjectSerializer.Meta):
        fields = SubjectSerializer.Meta.fields + ['students']
