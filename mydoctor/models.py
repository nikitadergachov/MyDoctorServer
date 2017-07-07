from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models import Model
from django.utils import timezone

from server.utcisoformat import utcisoformat


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now())

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    class CustomUserManager(BaseUserManager):
        def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
            """
            Creates and saves a User with the given email and password.
            """
            now = timezone.now()

            if not email:
                raise ValueError('The given email must be set')

            email = self.normalize_email(email)
            user = self.model(email=email,
                              is_staff=is_staff, is_active=True,
                              is_superuser=is_superuser, last_login=now,
                              date_joined=now, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_user(self, email, password=None, **extra_fields):
            return self._create_user(email, password, False, False, **extra_fields)

        def create_superuser(self, email, password, **extra_fields):
            return self._create_user(email, password, True, True, **extra_fields)


class Patient(models.Model):
    name = models.CharField(verbose_name='ФИО', max_length=60)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=12)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    insurance_number = models.CharField(verbose_name='Номер страхового полиса', max_length=20, unique=True)
    doctor = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    DOB = models.DateField(verbose_name='Дата рождения', default=timezone.now(), )
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', default=timezone.now())
    password = models.CharField('Пароль', max_length=128)

    def __str__(self):
        return self.name


class Analysis(models.Model):
    patient = models.ForeignKey(Patient)
    name = models.CharField(verbose_name='Название анализа', max_length=100)
    description = models.CharField(verbose_name='Описание анализа', max_length=200)
    date_appointment = models.DateTimeField(verbose_name='Дата назначения', default=timezone.now())


class VisitDoctor(models.Model):
    name_doctor = models.CharField(verbose_name='Тип врача', max_length=60)
    description = models.CharField(verbose_name='Дополнительная информация', max_length=200)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_appointment = models.DateTimeField(verbose_name='Дата назначения', default=timezone.now())


class Medicine(models.Model):
    AFTER_MEALS = [
        ('Независимо', 'Независимо'),
        ('До еды', 'До еды'),
        ('После еды', 'После еды'),
        ('Во время еды', 'Во время еды'),
    ]

    name = models.CharField(verbose_name='Название препарата', max_length=60)
    type = models.CharField(verbose_name='Тип медикамента', max_length=60)
    method_reception = models.CharField(verbose_name='Способ приёма', max_length=60)
    start_date = models.DateField(verbose_name='Дата начала приёма')
    end_date = models.DateField(verbose_name='Дата окончания')
    dosage = models.CharField(verbose_name='Дозировка', max_length=20)
    number_medicines = models.IntegerField(verbose_name='Количество')
    number_of_receptions_per_day = models.IntegerField(verbose_name='Количество применений в день')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(verbose_name='Дополнительная информация', max_length=200)
    after_meals = models.CharField(verbose_name='До еды?', max_length=20, choices=AFTER_MEALS)
    date_appointment = models.DateTimeField(verbose_name='Дата назначения', default=timezone.now())


class Procedure(models.Model):
    name = models.CharField(verbose_name='Название процедуры', max_length=60)
    description = models.CharField(verbose_name='Дополнительная информация', max_length=200)
    number = models.IntegerField(verbose_name='Количество процедур')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_appointment = models.DateTimeField(verbose_name='Дата назначения', default=timezone.now())
