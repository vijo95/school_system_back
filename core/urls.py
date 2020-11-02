from django.urls import path
from . views import (
    HomeView, StudentOrTeacherView, CreateTestView,
    TestDetailView, StudentTestDetailView,
    ProfileView, SubjectTestDetailView, StudentSubjectTestDetailView,
    CreateTaskView, TaskDetailView, StudentTaskDetailView,
    SubjectTaskDetailView, StudentSubjectTaskDetailView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create-profile/', StudentOrTeacherView.as_view(), name='create-profile'),
    path('profile/', ProfileView.as_view(), name="profile"),

    path('subject-test-detail/<id>/', SubjectTestDetailView.as_view(), name="subject-test-detail"),
    path('subject-task-detail/<id>/', SubjectTaskDetailView.as_view(), name='subject-task-detail'),

    path('student-subject-test-detail/<id>/', StudentSubjectTestDetailView.as_view(), name='student-subject-test-detail'),
    path('student-subject-task-detail/<id>/', StudentSubjectTaskDetailView.as_view(), name='student-subject-task-detail'),

    path('create-test/', CreateTestView.as_view(), name='create-test'),
    path('test-detail/<id>/', TestDetailView.as_view(), name="test-detail"),
    path('student-test-detail/<id>/', StudentTestDetailView.as_view(), name="student-test-detail"),

    path('create-task/', CreateTaskView.as_view(), name='create-task'),
    path('task-detail/<id>/', TaskDetailView.as_view(), name='task-detail'),
    path('student-task-detail/<id>/', StudentTaskDetailView.as_view(), name='student-task-detail'),
]
