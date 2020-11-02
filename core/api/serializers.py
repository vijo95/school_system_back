from rest_framework import serializers
from core.models import (
    StudentTask, StudentTest, Student, Teacher,
    TeacherDNI, StudentDNI, Year, Division,
    Subject, Test, StudentSubject, Task
)


class StudentDNISerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDNI
        fields = ['dni']


class TeacherDNISerializer(serializers.ModelSerializer):

    dni_name = serializers.ReadOnlyField(source='dni.dni')

    class Meta:
        model = TeacherDNI
        fields = ['dni']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'user','name','lastname',
            'dni_name','entry_year',
            'current_year','exit_year'
        ]


class TeacherSerializer(serializers.ModelSerializer):
    dni_name = serializers.ReadOnlyField(source='dni.dni')
    class Meta:
        model = Teacher
        fields = [
            'user','name','lastname',
            'dni_name', 'entry_year',
            'exit_year'
        ]


class YearSerializer(serializers.ModelSerializer):

    division_name = serializers.ReadOnlyField(source='division.name')

    class Meta:
        model = Year
        fields = [
            'id','year','division_name'
        ]


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['name']


class SubjectSerializer(serializers.ModelSerializer):
    year_year = serializers.ReadOnlyField(source='year.year')
    year_division = serializers.ReadOnlyField(source='year.division.name')
    class Meta:
        model = Subject
        fields = [
            'id','teacher',
            'name','year_year',
            'year_division'
        ]


class StudentSubjectSerializer(serializers.ModelSerializer):
    subject_id = serializers.ReadOnlyField(source='subject.id')
    subject_name = serializers.ReadOnlyField(source='subject.name')
    subject_year = serializers.ReadOnlyField(source='subject.year.year')
    subject_year_division = serializers.ReadOnlyField(source='subject.year.division.name')
    class Meta:
        model = StudentSubject
        fields = [
            'student','subject_name',
            'subject_year','average',
            'passed','subject_year_division',
            'subject_id'
        ]


class TaskSerializer(serializers.ModelSerializer):
    subject_id = serializers.ReadOnlyField(source='subject.id')
    subject_name = serializers.ReadOnlyField(source='subject.name')
    subject_year = serializers.ReadOnlyField(source='subject.year.year')
    subject_year_division = serializers.ReadOnlyField(source='subject.year.division.name')
    class Meta:
        model = Task
        fields = [
            'title','created_date',
            'text','teacher','due',
            'subject_name',
            'subject_year',
            'subject_year_division',
            'subject_id','id'
        ]


class StudentTaskSerializer(serializers.ModelSerializer):
    subject_id = serializers.ReadOnlyField(source='task.subject.id')
    student_name = serializers.ReadOnlyField(source='student.name')
    student_last = serializers.ReadOnlyField(source='student.lastname')
    title = serializers.ReadOnlyField(source='task.title')
    created_date = serializers.ReadOnlyField(source='task.created_date')
    due = serializers.ReadOnlyField(source='task.due')
    subject_name = serializers.ReadOnlyField(source='task.subject.name')
    subject_year = serializers.ReadOnlyField(source='task.subject.year.year')
    subject_year_division = serializers.ReadOnlyField(source='task.subject.year.division.name')
    text = serializers.ReadOnlyField(source="task.text")
    class Meta:
        model = StudentTask
        fields = [
            'student_name','student_last',
            'student','subject_name',
            'title','created_date',
            'grade','delivered','due',
            'subject_year','text',
            'subject_year_division',
            'id','subject_id'
        ]


class TestSerializer(serializers.ModelSerializer):
    subject_id = serializers.ReadOnlyField(source='subject.id')
    subject_name = serializers.ReadOnlyField(source='subject.name')
    subject_year = serializers.ReadOnlyField(source='subject.year.year')
    subject_year_division = serializers.ReadOnlyField(source='subject.year.division.name')
    class Meta:
        model = Test
        fields = [
            'id','teacher',
            'title','date',
            'subject_name',
            'subject_year',
            'subject_year_division',
            'subject_id',
        ]


class StudentTestSerializer(serializers.ModelSerializer):
    subject_id = serializers.ReadOnlyField(source='test.subject.id')
    student_name = serializers.ReadOnlyField(source='student.name')
    student_last = serializers.ReadOnlyField(source='student.lastname')
    title = serializers.ReadOnlyField(source='test.title')
    date = serializers.ReadOnlyField(source='test.date')
    subject_name = serializers.ReadOnlyField(source='test.subject.name')
    subject_year = serializers.ReadOnlyField(source='test.subject.year.year')
    subject_year_division = serializers.ReadOnlyField(source='test.subject.year.division.name')
    class Meta:
        model = StudentTest
        fields = [
            'student','date',
            'grade','title',
            'subject_name',
            'subject_name',
            'subject_year',
            'subject_year_division',
            'student_name',
            'student_last',
            'id','subject_id'
        ]
