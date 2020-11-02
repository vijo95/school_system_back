from django.urls import path
from . api import (
    HomeAPIView, StudentOrTeacherAPIView,
    StudentTestDetailAPIView,
    StudentTaskDetailAPIView, SubjectsAPIView,
    CreateTaskAPIView, CreateTestAPIView,
    UpdateStudentTaskGradeAPIView,
    UpdateStudentTestGradeAPIView,
    CreateProfileAPIView,
)

urlpatterns = [
    path('',HomeAPIView.as_view(), name='home'),
    path('student-teacher/', StudentOrTeacherAPIView.as_view(), name="student-teacher"),
    path('create-profile/', CreateProfileAPIView.as_view(), name="create-profile"),

    path('subjects/', SubjectsAPIView.as_view(), name="subjects"),

    path('create-task/', CreateTaskAPIView.as_view(), name="create-task"),
    path('create-test/', CreateTestAPIView.as_view(), name="create-test"),

    path('student-task-detail/', StudentTaskDetailAPIView.as_view(), name='student-task-detail'),
    path('student-test-detail/', StudentTestDetailAPIView.as_view(), name='student-test-detail'),

    path('update-student-task/', UpdateStudentTaskGradeAPIView.as_view(), name='update-student-task'),
    path('update-student-test/', UpdateStudentTestGradeAPIView.as_view(), name='update-student-test')
]
