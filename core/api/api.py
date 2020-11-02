from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.core import serializers
from core.models import (
    StudentTask, StudentTest, Student, Teacher,
    TeacherDNI, StudentDNI, Year, Division,
    Subject, Test, StudentSubject, Task
)
from . serializers import (
    StudentDNISerializer, TeacherDNISerializer,
    StudentSerializer, TeacherSerializer,
    YearSerializer, DivisionSerializer,
    SubjectSerializer, StudentSubjectSerializer,
    TestSerializer, StudentTestSerializer,
    TaskSerializer, StudentTaskSerializer
)

class HomeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        try:
            student = Student.objects.get(user=self.request.user)

            task_list_student = []
            for task in StudentTask.objects.filter(student=student).order_by('-task__due'):
                task_list_student.append(StudentTaskSerializer(task).data)

            test_list_student = []
            for test in StudentTest.objects.filter(student=student).order_by('-test__date'):
                test_list_student.append(StudentTestSerializer(test).data)

            context = {
                'student': True,
                'teacher': False,
                'task_list_student': task_list_student,
                'test_list_student': test_list_student,
            }
        except:
            try:
                teacher = Teacher.objects.get(user=self.request.user)

                test_list_teacher = []
                for test in Test.objects.filter(teacher=teacher).order_by('-date'):
                    test_list_teacher.append(TestSerializer(test).data)

                task_list_teacher = []
                for task in Task.objects.filter(teacher=teacher).order_by('-due'):
                    task_list_teacher.append(TaskSerializer(task).data)

                context = {
                    'student': False,
                    'teacher': True,
                    'task_list_teacher':task_list_teacher,
                    'test_list_teacher':test_list_teacher,
                }
            except:
                return Response(
                    {'message':'Debes crearte un perfil'},
                    status=HTTP_200_OK
                )

        return Response(context,status=HTTP_200_OK)


class StudentOrTeacherAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, *args, **kwargs):
        try:
            student = StudentDNI.objects.get(dni=int(self.request.user.username))
            student = True
        except:
            student = False

        try:
            teacher = TeacherDNI.objects.get(dni=int(self.request.user.username))
            teacher = True
        except:
            teacher = False

        if student:
            year_list = []
            for year in Year.objects.all():
                year_list.append(YearSerializer(year).data)

            context = {
                'student': True,
                'year_list': year_list
            }
        elif teacher:
            context = {'teacher': True}
        else:
            context = {'nothing': True}

        try:
            student_profile = Student.objects.get(user=self.request.user)
            got_student_profile = True
        except:
            got_student_profile = False

        try:
            teacher_profile = Teacher.objects.get(user=self.request.user)
            got_teacher_profile = True
        except:
            got_teacher_profile = False


        if got_student_profile or got_teacher_profile:
            return Response(
                {'message':'Ya tienes un perfil'},
                status=HTTP_200_OK
            )

        return Response(context,status=HTTP_200_OK)


class CreateProfileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            student = StudentDNI.objects.get(dni=int(self.request.user.username))
            student_dni = student
            student = True
        except:
            student = False

        try:
            teacher = TeacherDNI.objects.get(dni=int(self.request.user.username))
            teacher_dni = teacher
            teacher = True
        except:
            teacher = False

        name = request.data.get('name', None)
        last_name = request.data.get('last_name', None)
        dni = request.data.get('dni', None)
        entry_year = request.data.get('entry_year', None)

        if name is None or last_name is None or dni is None or entry_year is None:
            return Response(
                {'message':'Por favor complete el formulario correctamente'},
                status=HTTP_400_BAD_REQUEST
            )

        if student:
            current_year = request.data.get('current_year', None)

            if int(self.request.user.username) != int(dni):
                return Response(
                    {'message':'Ese no es tu DNI'},
                    status=HTTP_400_BAD_REQUEST
                )

            if current_year is None:
                return Response(
                    {'message':'Por favor complete el campo Año Actual'},
                    status=HTTP_400_BAD_REQUEST
                )

            year = Year.objects.get(id=int(current_year))

            student_profile = Student.objects.create(
                user = self.request.user,
                name=name, lastname=last_name,
                dni=student_dni, entry_year=entry_year,
                current_year=year
            )
            student_profile.save()

            subject_list = Subject.objects.filter(year=year)

            for subject_obj in subject_list:
                student_subject = StudentSubject.objects.create(
                    student=student_profile,
                    subject=subject_obj,
                )
                student_subject.save()

            return Response(
                {'message':'Perfil creado exitosamente'},
                status=HTTP_200_OK
            )
        elif teacher:
            if int(self.request.user.username) != int(dni):
                return Response(
                    {'message':'Ese no es tu DNI'},
                    status=HTTP_400_BAD_REQUEST
                )

            teacher_profile = Teacher.objects.create(
                user=self.request.user,
                name=name, lastname=last_name,
                dni=teacher_dni, entry_year=entry_year,
            )
            teacher_profile.save()

            return Response(
                {'message':'Perfil creado exitosamente'},
                status=HTTP_200_OK
            )

        return Response(
            {'message':'No estás registrado como alumno o profesor'},
            status=HTTP_200_OK
        )


class SubjectsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        try:
            student = Student.objects.get(user=self.request.user)

            subject_list_student = []
            for subject in StudentSubject.objects.filter(student=student):
                subject_list_student.append(StudentSubjectSerializer(subject).data)

            context = {
                'student': True,
                'teacher': False,
                'subject_list_student': subject_list_student,
            }
        except:
            try:
                teacher = Teacher.objects.get(user=self.request.user)

                subject_list_teacher = []
                for subject in Subject.objects.filter(teacher=teacher):
                    subject_list_teacher.append(SubjectSerializer(subject).data)

                context = {
                    'student': False,
                    'teacher': True,
                    'subject_list_teacher': subject_list_teacher,
                }
            except:
                return Response(
                    {'message':'Debes crearte un perfil'},
                    status=HTTP_400_BAD_REQUEST
                )

        return Response(context,status=HTTP_200_OK)


# ----- TASKS API ----- #
class CreateTaskAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        try:
            teacher = TeacherDNI.objects.get(dni=int(self.request.user.username))
            teacher = True
        except:
            teacher = False

        if teacher:
            title = request.data.get('title', None)
            text = request.data.get('text', None)
            date_day = request.data.get('date_day', None)
            date_month = request.data.get('date_month', None)
            date_year = request.data.get('date_year', None)
            subject = request.data.get('subject', None)

            subject = subject.split(',')

            teacher_obj = Teacher.objects.get(user=self.request.user)
            division_obj = Division.objects.get(name=subject[2])
            year_obj = Year.objects.get(year=subject[1],division=division_obj)

            subject_obj = Subject.objects.get(
                teacher=teacher_obj,
                name=subject[0],
                year=year_obj
            )

            task = Task.objects.create(
                teacher=teacher_obj,
                due=date_year+"-"+date_month+"-"+date_day,
                subject=subject_obj,
                title=title, text=text
            )

            task.save()

            student_list = Student.objects.filter(current_year=year_obj)

            for student in student_list:
                student_task = StudentTask.objects.create(student=student,task=task)
                student_task.save()

            return Response(
                {'message':'Trabajo creado correctamente'},
                status=HTTP_200_OK
            )

        return Response(
            {'message':'Por favor complete el formulario correctamente'},
            status=HTTP_400_BAD_REQUEST
        )


class StudentTaskDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        try:
            teacher = Teacher.objects.get(user=self.request.user)
            task = Task.objects.get(id=id, teacher=teacher)

            student_task_list = []
            for student_task in StudentTask.objects.filter(task=task).order_by('student__lastname'):
                student_task_list.append(StudentTaskSerializer(student_task).data)

            task = TaskSerializer(task).data

            context = {
                'task':task,
                'student_task_list': student_task_list,
            }
        except Exception as e:
            print(e)
            return Response(
                {'message':'No tienes los permisos para aceder a esta página'},
                status=HTTP_400_BAD_REQUEST
            )

        return Response(context,status=HTTP_200_OK)


class UpdateStudentTaskGradeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        student_task_grade_list = request.data.get('student_task_grade_list')
        task_id = request.data.get('task_id')
        try:
            teacher = Teacher.objects.get(user=self.request.user)
            task = Task.objects.get(teacher=teacher, id=int(task_id))

            for student_task_grade in student_task_grade_list:
                student_task = StudentTask.objects.get(id=int(student_task_grade["student_task_id"]))

                if "student_new_grade" in student_task_grade and "student_new_delivered" in student_task_grade:
                    if int(student_task_grade["student_new_grade"]) == 0:
                        student_task.grade = None
                        student_task.delivered = None
                        student_task.save()
                    else:
                        student_task.grade = int(student_task_grade["student_new_grade"])
                        student_task.delivered = student_task_grade["student_new_delivered"]
                        student_task.save()
                elif "student_new_grade" in student_task_grade:
                    if int(student_task_grade["student_new_grade"]) == 0:
                        student_task.grade = None
                        student_task.save()
                    else:
                        student_task.grade = int(student_task_grade["student_new_grade"])
                        student_task.save()
                else:
                    if student_task_grade["student_new_delivered"] == None:
                        student_task.grade = None
                        student_task.delivered = None
                        student_task.save()
                    else:
                        student_task.delivered = student_task_grade["student_new_delivered"]
                        student_task.save()

            return Response(
                {'message':'Notas cargadas correctamente'},
                status=HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'message':'No tienes los permisos para aceder a esta página'},
                status=HTTP_400_BAD_REQUEST
            )


# ----- TESTS API ----- #
class CreateTestAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        try:
            teacher = TeacherDNI.objects.get(dni=int(self.request.user.username))
            teacher = True
        except:
            teacher = False

        if teacher:
            title = request.data.get('title', None)
            date_day = request.data.get('date_day', None)
            date_month = request.data.get('date_month', None)
            date_year = request.data.get('date_year', None)
            subject = request.data.get('subject', None)

            subject = subject.split(',')

            teacher_obj = Teacher.objects.get(user=self.request.user)
            division_obj = Division.objects.get(name=subject[2])
            year_obj = Year.objects.get(year=subject[1],division=division_obj)

            subject_obj = Subject.objects.get(
                teacher=teacher_obj,
                name=subject[0],
                year=year_obj
            )

            test = Test.objects.create(
                teacher=teacher_obj,
                date=date_year+"-"+date_month+"-"+date_day,
                subject=subject_obj,
                title=title
            )
            test.save()

            student_list = Student.objects.filter(current_year=year_obj)

            for student in student_list:
                student_test = StudentTest.objects.create(student=student,test=test)
                student_test.save()

            return Response(
                {'message':'Exámen creado correctamente'},
                status=HTTP_200_OK
            )

        return Response(
            {'message':'Por favor complete el formulario correctamente'},
            status=HTTP_400_BAD_REQUEST
        )


class StudentTestDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request,*args, **kwargs):
        id = request.data.get('id', None)
        try:

            teacher = Teacher.objects.get(user=self.request.user)
            test = Test.objects.get(id=id,teacher=teacher)

            student_test_list = []
            for student_test in StudentTest.objects.filter(test=test).order_by('student__lastname'):
                student_test_list.append(StudentTestSerializer(student_test).data)

            test = TestSerializer(test).data

            context = {
                'test':test,
                'student_test_list': student_test_list,
            }
        except:
            return Response(
                {'message':'No tienes los permisos para aceder a esta página'},
                status=HTTP_400_BAD_REQUEST
            )

        return Response(context,status=HTTP_200_OK)


class UpdateStudentTestGradeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        student_test_grade_list = request.data.get('student_test_grade_list')
        test_id = request.data.get('test_id')
        try:
            teacher = Teacher.objects.get(user=self.request.user)
            test = Test.objects.get(teacher=teacher, id=int(test_id))

            for student_test_grade in student_test_grade_list:
                student_test = StudentTest.objects.get(id=int(student_test_grade["student_test_id"]))

                if "student_new_grade" in student_test_grade:
                    if int(student_test_grade["student_new_grade"]) == 0:
                        student_test.grade = None
                        student_test.save()
                    else:
                        student_test.grade = int(student_test_grade["student_new_grade"])
                        student_test.save()

            return Response(
                {'message':'Notas cargadas correctamente'},
                status=HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'message':'No tienes los permisos para aceder a esta página'},
                status=HTTP_400_BAD_REQUEST
            )
