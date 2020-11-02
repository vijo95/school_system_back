from django.contrib import admin
from . models import (
        Subject, Student,
        Year, StudentSubject,Teacher,
        Division, Task, Test,
        StudentTask, StudentTest,
        StudentDNI, TeacherDNI
)


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'created_date',
        'teacher',
        'subject',
        'due',
    ]
    readonly_fields = ['created_date']

class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'teacher',
        'year',
    ]

class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'lastname',
        'dni',
        'current_year',
        'entry_year',
        'exit_year',
    ]

class YearAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'year',
        'division',
    ]

class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'subject',
    ]

class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'lastname',
        'dni',
        'entry_year',
        'exit_year',
    ]

class DivisionAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]

class TestAdmin(admin.ModelAdmin):
    list_display = [
        'subject',
        'teacher',
        'title',
        'date',
    ]

class StudentTaskAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'task',
        'delivered',
    ]

class StudentTestAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'test',
        'grade',
    ]

admin.site.register(Subject,SubjectAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Year,YearAdmin)
admin.site.register(StudentSubject,StudentSubjectAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Division,DivisionAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Test,TestAdmin)
admin.site.register(StudentTask,StudentTaskAdmin)
admin.site.register(StudentTest,StudentTestAdmin)
admin.site.register(StudentDNI)
admin.site.register(TeacherDNI)
