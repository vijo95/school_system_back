from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from . models import (
    StudentTask, StudentTest, Student, Teacher,
    TeacherDNI, StudentDNI, Year, Division,
    Subject, Test, StudentSubject, Task
)
from . forms import (
    CreateProfileForm, CreateTestForm,
    StudentTestGradeForm, CreateTaskForm,
    StudentTaskGradeForm
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


# Aux Funcs
def clean_path_id_subject_test(path):
    return (path.replace("/subject-test-detail/",""))[:-1]

def clean_path_id_subject_task(path):
    return (path.replace("/subject-task-detail/",""))[:-1]

def clean_path_id_student_subject_test(path):
    return (path.replace("/student-subject-test-detail/",""))[:-1]

def clean_path_id_student_subject_task(path):
    return (path.replace("/student-subject-task-detail/",""))[:-1]

def clean_path_id_test(path):
    return (path.replace("/test-detail/",""))[:-1]

def clean_path_id_student_test(path):
    return (path.replace("/student-test-detail/",""))[:-1]

def clean_path_id_task(path):
    return (path.replace("/task-detail/",""))[:-1]

def clean_path_id_student_task(path):
    return (path.replace("/student-task-detail/",""))[:-1]


# Create your views here.


class HomeView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        try:
            student = Student.objects.get(user=self.request.user)
            context = {
                'student': True,
                'teacher': False,
                'task_list_student': StudentTask.objects.filter(student=student).order_by('-task__due'),
                'test_list_student': StudentTest.objects.filter(student=student).order_by('-test__date')
            }
        except:
            try:
                teacher = Teacher.objects.get(user=self.request.user)

                context = {
                    'student': False,
                    'teacher': True,
                    'test_list_teacher': Test.objects.filter(teacher=teacher).order_by('-date'),
                    'task_list_teacher': Task.objects.filter(teacher=teacher).order_by('-due'),
                }
            except:
                messages.warning(self.request, "Debes crearte un perfil")
                return redirect('core:create-profile')

        return render(self.request, "home.html", context)


class StudentOrTeacherView(LoginRequiredMixin,View):

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
            context = {
                'student': True,
                'year_list': Year.objects.all()
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
            return redirect('core:home')

        return render(self.request, "create_profile.html", context)

    def post(self, *args, **kwargs):
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

        form = CreateProfileForm(self.request.POST or None)

        if form.is_valid():
            if student:
                name = form.cleaned_data.get('name')
                last_name = form.cleaned_data.get('last_name')
                dni = form.cleaned_data.get('dni')
                entry_year = form.cleaned_data.get('entry_year')
                current_year = form.cleaned_data.get('current_year')

                if int(self.request.user.username) != int(dni):
                    messages.error(self.request, "Ese no es tu DNI")
                    return redirect('core:create-profile')

                if not current_year or current_year == '':
                    messages.error(self.request, "Por favor complete el campo Año Actual")
                    return redirect('core:create-profile')

                current_year = current_year.split(',')
                division = Division.objects.get(name=current_year[1])

                try:
                    division = Division.objects.get(name=current_year[1])
                    year = Year.objects.get(year=int(current_year[0]), division=division)
                    student_dni = StudentDNI.objects.get(dni=int(dni))
                except:
                    messages.error(self.request, "Por favor complete el formulario correctamente")
                    return redirect('core:create-profile')

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

                messages.success(self.request, "Perfil creado exitosamente")
                return redirect('core:home')
            elif teacher:
                name = form.cleaned_data.get('name')
                last_name = form.cleaned_data.get('last_name')
                dni = form.cleaned_data.get('dni')
                entry_year = form.cleaned_data.get('entry_year')

                if int(self.request.user.username) != int(dni):
                    messages.error(self.request, "Ese no es tu DNI")
                    return redirect('core:create-profile')

                try:
                    teacher_dni = TeacherDNI.objects.get(dni=int(dni))
                except:
                    messages.error(self.request, "Ese no es tu DNI")
                    return redirect('core:create-profile')

                teacher_dni = TeacherDNI.objects.get(dni=int(dni))
                teacher_profile = Teacher.objects.create(
                    user=self.request.user,
                    name=name, lastname=last_name,
                    dni=teacher_dni, entry_year=entry_year,
                )
                teacher_profile.save()

                return redirect('core:home')

        messages.error(self.request, "Por favor complete el formulario correctamente")
        return redirect('core:create-profile')


class ProfileView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        try:
            student = Student.objects.get(user=self.request.user)
            student_subject_list = StudentSubject.objects.filter(student=student)
            context = {
                'student': True,
                'student_subject_list': student_subject_list,
            }
        except:
            try:
                teacher = Teacher.objects.get(user=self.request.user)
                subject_list = Subject.objects.filter(teacher=teacher)
                context = {
                    'teacher': True,
                    'subject_list': subject_list,
                }
            except:
                messages.warning(self.request, "Debes crearte un perfil")
                return redirect('core:create-profile')
        return render(self.request, "profile.html", context)


class SubjectTestDetailView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        id = clean_path_id_subject_test(self.request.path)
        try:
            teacher = Teacher.objects.get(user=self.request.user)
            subject = Subject.objects.get(id=id, teacher=teacher)
            student_subject_list = StudentSubject.objects.filter(subject=subject).order_by('student__lastname')
            student_test_list = StudentTest.objects.filter(test__subject=subject).order_by('test__date')
            context = {
                'student_subject_list': student_subject_list,
                'student_test_list': student_test_list,
                'subject': subject,
            }
        except:
            messages.warning(self.request, "No tienes los permisos para aceder a esta página")
            return redirect('core:create-profile')

        return render(self.request, "subject_test_detail.html", context)


class SubjectTaskDetailView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        id = clean_path_id_subject_task(self.request.path)
        try:
            teacher = Teacher.objects.get(user=self.request.user)
            subject = Subject.objects.get(id=id, teacher=teacher)
            student_subject_list = StudentSubject.objects.filter(subject=subject).order_by('student__lastname')
            student_task_list = StudentTask.objects.filter(task__subject=subject).order_by('task__due')
            context = {
                'student_subject_list': student_subject_list,
                'student_task_list': student_task_list,
                'subject': subject,
            }
        except:
            messages.warning(self.request, "No tienes los permisos para aceder a esta página")
            return redirect('core:create-profile')

        return render(self.request, "subject_task_detail.html", context)


class StudentSubjectTestDetailView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        id = clean_path_id_student_subject_test(self.request.path)
        try:
            student = Student.objects.get(user=self.request.user)
            student_subject = StudentSubject.objects.get(id=id, student=student)
            student_test_list = StudentTest.objects.filter(
                test__subject=student_subject.subject, student=student
            )
            context = {
                'student_subject': student_subject,
                'student_test_list': student_test_list,
            }
        except:
            messages.error(self.request, "No tienes los permisos para aceder a esta página")
            return redirect('core:home')

        return render(self.request, "student_subject_test_detail.html", context)


class StudentSubjectTaskDetailView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        id = clean_path_id_student_subject_task(self.request.path)
        try:
            student = Student.objects.get(user=self.request.user)
            student_subject = StudentSubject.objects.get(id=id, student=student)
            student_task_list = StudentTask.objects.filter(
                task__subject=student_subject.subject, student=student
            )
            context = {
                'student_subject': student_subject,
                'student_task_list': student_task_list,
            }
        except:
            messages.error(self.request, "No tienes los permisos para aceder a esta página")
            return redirect('core:home')

        return render(self.request, "student_subject_task_detail.html", context)


class CreateTestView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        try:
            teacher = TeacherDNI.objects.get(dni=int(self.request.user.username))
            teacher = True
        except:
            teacher = False

        if teacher:
            days = list(range(1,32))
            months = [
                'Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio',
                'Agosto','Septimebre','Octubre','Noviembre','Diciembre'
            ]
            years = list(range(2020,2101))

            teacher_obj = Teacher.objects.get(user=self.request.user)
            subject_list = Subject.objects.filter(teacher=teacher_obj)

            context = {
                'test_form': CreateTestForm(),
                'days': days,
                'months': months,
                'years': years,
                'subject_list': subject_list,
            }

            return render(self.request, "create_test.html", context)
        else:
            messages.error(self.request, "No estás autorizado para acceder a esa página")
            return redirect('core:home')

    def post(self, *args, **kwargs):
        form = CreateTestForm(self.request.POST or None)

        if form.is_valid():
            date_day = form.cleaned_data.get('date_day')
            date_month = form.cleaned_data.get('date_month')
            date_year = form.cleaned_data.get('date_year')
            title = form.cleaned_data.get('title')

            subject = form.cleaned_data.get('subject')
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

            messages.success(self.request, "Examen creado correctamente")
            return redirect('core:home')

        messages.error(self.request, "Por favor complete el formulario correctamente")
        return redirect('core:create-test')


class TestDetailView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        id = clean_path_id_test(self.request.path)
        try:
            teacher = Teacher.objects.get(user=self.request.user)
            test = Test.objects.get(teacher=teacher, id=id)
            context = {
                'test_date': test.date,
                'test_title': test.title,
                'test': test.subject.name + " de " + str(test.subject.year.year) + "° " + test.subject.year.division.name,
                'student_test_list': StudentTest.objects.filter(test=test).order_by('student__lastname')
            }
        except:
            messages.error(self.request,"No tienes permiso para acceder a esta página")
            return redirect('core:home')

        return render(self.request, "test_detail.html", context)


class StudentTestDetailView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        try:
            id = clean_path_id_student_test(self.request.path)
            teacher = Teacher.objects.get(user=self.request.user)
            student_test = StudentTest.objects.get(id=id)
            if student_test.test.teacher.id == teacher.id:
                context = {
                    'student_test': student_test,
                    'grade': student_test.grade
                }
        except:
            messages.error(self.request,"No tienes permiso para acceder a esta página")
            return redirect('core:home')

        return render(self.request, "student_test_detail.html", context)

    def post(self, *args, **kwargs):
        form = StudentTestGradeForm(self.request.POST or None)
        id = clean_path_id_student_test(self.request.path)

        if form.is_valid():
            grade = form.cleaned_data.get('grade')
            try:
                student_test = StudentTest.objects.get(id=id)
                student_test.grade = grade
                student_test.save()
                test_id = student_test.test.id

                messages.success(self.request,"Se ha cargado la nota exitosamente")
                return redirect('core:test-detail',test_id)
            except:
                messages.error(self.request,"No se pudo cargar la nota")
                return redirect('core:student-test-detail',id)

        messages.error(self.request,"Debes agregar una nota")
        return redirect('core:student-test-detail',id)


class CreateTaskView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        try:
            teacher = TeacherDNI.objects.get(dni=int(self.request.user.username))
            teacher = True
        except:
            teacher = False

        if teacher:
            days = list(range(1,32))
            months = [
                'Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio',
                'Agosto','Septimebre','Octubre','Noviembre','Diciembre'
            ]
            years = list(range(2020,2101))

            teacher_obj = Teacher.objects.get(user=self.request.user)
            subject_list = Subject.objects.filter(teacher=teacher_obj)

            context = {
                'test_form': CreateTaskForm(),
                'days': days,
                'months': months,
                'years': years,
                'subject_list': subject_list,
            }

            return render(self.request, "create_task.html", context)
        else:
            messages.error(self.request, "No estás autorizado para acceder a esa página")
            return redirect('core:home')

    def post(self, *args, **kwargs):
        form = CreateTaskForm(self.request.POST or None)
        print(form)
        if form.is_valid():
            date_day = form.cleaned_data.get('date_day')
            date_month = form.cleaned_data.get('date_month')
            date_year = form.cleaned_data.get('date_year')
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')

            subject = form.cleaned_data.get('subject')
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

            messages.success(self.request, "Trabajo creado correctamente")
            return redirect('core:home')

        messages.error(self.request, "Por favor complete el formulario correctamente")
        return redirect('core:create-task')


class TaskDetailView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        id = clean_path_id_task(self.request.path)
        try:
            teacher = Teacher.objects.get(user=self.request.user)
            task = Task.objects.get(teacher=teacher, id=id)
            student_task_list = StudentTask.objects.filter(task=task).order_by('student__lastname')
            context = {
                'task': task,
                'student_task_list': student_task_list
            }
        except:
            messages.error(self.request,"No tienes permiso para acceder a esta página")
            return redirect('core:home')

        return render(self.request, "task_detail.html", context)


class StudentTaskDetailView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        try:
            id = clean_path_id_student_task(self.request.path)
            teacher = Teacher.objects.get(user=self.request.user)
            student_task = StudentTask.objects.get(id=id)
            if student_task.task.teacher.id == teacher.id:
                context = {
                    'student_task': student_task,
                    'grade': student_task.grade,
                    'delivered': student_task.delivered
                }
        except Exception as e:
            print(e)
            messages.error(self.request,"No tienes permiso para acceder a esta página")
            return redirect('core:home')

        return render(self.request, "student_task_detail.html", context)

    def post(self, *args, **kwargs):
        form = StudentTaskGradeForm(self.request.POST or None)
        id = clean_path_id_student_task(self.request.path)

        if form.is_valid():
            grade = form.cleaned_data.get('grade')
            delivered = form.cleaned_data.get('delivered')
            try:
                student_task = StudentTask.objects.get(id=id)
                if delivered == 'true':
                    student_task.grade = grade
                    student_task.delivered = True
                elif delivered == 'false':
                    student_task.grade = None
                    student_task.delivered = False
                student_task.save()
                task_id = student_task.task.id

                messages.success(self.request,"Se ha calificado el trabajo correctamente")
                return redirect('core:task-detail',task_id)
            except:
                messages.error(self.request,"No se pudo calificar el trabajo")
                return redirect('core:student-task-detail',id)

        messages.error(self.request,"Debes agregar una nota")
        return redirect('core:student-task-detail',id)
