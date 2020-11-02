from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.shortcuts import reverse

# Create your models here.

class StudentDNI(models.Model):
    dni = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.dni}"


class TeacherDNI(models.Model):
    dni = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.dni}"


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True)
    name = models.CharField(max_length=64, blank=True,null=True)
    lastname = models.CharField(max_length=64, blank=True,null=True)
    dni = models.ForeignKey(
        'StudentDNI',
        on_delete=models.SET_NULL,
        blank=True,null=True)
    entry_year = models.IntegerField(blank=True,null=True)
    current_year = models.ForeignKey(
        'Year',on_delete=models.SET_NULL,
        blank=True,null=True)
    exit_year = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.name}, {self.lastname}"


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True)
    name = models.CharField(max_length=64, blank=True,null=True)
    lastname = models.CharField(max_length=64, blank=True,null=True)
    dni = models.ForeignKey(
        'TeacherDNI',
        on_delete=models.SET_NULL,
        blank=True,null=True)
    entry_year = models.IntegerField(blank=True,null=True)
    exit_year = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.lastname}, {self.name}"


class Year(models.Model):
    year = models.IntegerField(blank=True,null=True)
    division = models.ForeignKey(
        'Division',
        on_delete=models.SET_NULL,
        blank=True, null=True)

    def __str__(self):
        return f"{self.year}° ({self.division})"


class Division(models.Model):
    name = models.CharField(max_length=32,blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Subject(models.Model):
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        blank=True, null=True)
    name = models.CharField(max_length=32, blank=True,null=True)
    year = models.ForeignKey(
        'Year', on_delete=models.SET_NULL,
        blank=True,null=True)

    def __str__(self):
        return f"{self.name} de {self.year}"

    def get_absolute_url(self):
        return reverse("core:subject-test-detail", kwargs={
            'id': self.id
        })

    def get_absolute_url_task(self):
        return reverse("core:subject-task-detail", kwargs={
            'id': self.id
        })


class StudentSubject(models.Model):
    student = models.ForeignKey(
        'Student', on_delete=models.CASCADE,
        blank=True, null=True)
    subject = models.ForeignKey(
        'Subject', on_delete=models.SET_NULL,
        blank=True,null=True)

    average = models.FloatField(blank=True,null=True)
    passed = models.BooleanField(blank=True,null=True)

    def __str__(self):
        return f"{self.student} | {self.subject}"

    def get_absolute_url(self):
        return reverse("core:student-subject-test-detail", kwargs={
            'id': self.id
        })

    def get_absolute_url_task(self):
        return reverse("core:student-subject-task-detail", kwargs={
            'id': self.id
        })


class Test(models.Model):
    date = models.DateField(default=now)
    title = models.CharField(max_length=32, blank=True, null=True)
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        blank=True, null=True)
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.SET_NULL,
        blank=True, null=True)

    def __str__(self):
        return f"{self.title}, {self.subject.name} de {self.subject.year} | {self.date}"

    def get_absolute_url(self):
        return reverse("core:test-detail", kwargs={
            'id': self.id
        })


class StudentTest(models.Model):
    student = models.ForeignKey(
        'Student', on_delete=models.CASCADE,
        blank=True, null=True)
    test = models.ForeignKey(
        'Test', on_delete=models.CASCADE,
        blank=True,null=True)
    grade = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.test} | {self.grade}"

    def get_absolute_url(self):
        return reverse("core:student-test-detail", kwargs={
            'id': self.id
        })


class Task(models.Model):
    title = models.CharField(max_length=64,blank=True, null=True)
    created_date = models.DateTimeField(default=now)
    text = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        blank=True, null=True)
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.SET_NULL,
        blank=True, null=True)
    due = models.DateField()

    def __str__(self):
        return f"{self.title} | {self.subject}"

    def get_absolute_url(self):
        return reverse("core:task-detail", kwargs={
            'id': self.id
        })


class StudentTask(models.Model):
    student = models.ForeignKey(
        'Student', on_delete=models.CASCADE,
        blank=True, null=True)
    task = models.ForeignKey(
        'Task', on_delete=models.CASCADE,
        blank=True,null=True)
    grade = models.IntegerField(blank=True,null=True)
    delivered = models.BooleanField(blank=True,null=True)

    def __str__(self):
        return f"{self.student} | {self.task} | {self.delivered}"

    def get_absolute_url(self):
        return reverse("core:student-task-detail", kwargs={
            'id': self.id
        })
