import datetime
import random

from django.db import models
from django.utils import timezone

from mydoctor.models import Patient, MyUser


class TakenMedicine(models.Model):
    patient = models.ForeignKey(Patient, verbose_name='Пациент', on_delete=models.CASCADE)
    name_medicine = models.CharField(verbose_name='Название медикамента', max_length=60)
    number_of_necessary_medicine = models.IntegerField(
        verbose_name='Количество медикаметов которые необходимо принять')
    number_of_medication_taken = models.IntegerField(verbose_name='Количество принятых медикаметов')
    date_of_taking_medicine = models.DateField(verbose_name='Дата принятия медикатов')
    date_create = models.DateTimeField(verbose_name='Дата синхронизации', default=timezone.now())

    @staticmethod
    def generate_date():
        medicines = TakenMedicine


        patient = Patient.objects.get()

        name = "Анальгин"
        time = timezone.now()


        for x in range(20):
            time += datetime.timedelta(days=1)
            rand = random.choice([2, 3])
            med = TakenMedicine(patient=patient, name_medicine=name,
                                date_of_taking_medicine=time, number_of_necessary_medicine = 3,
                                number_of_medication_taken=rand)
            med.save()

        name = "Парацетамол"
        time = timezone.now()
        for x in range(20):
            time += datetime.timedelta(days=1)
            rand = random.choice([2, 3])
            med = TakenMedicine(patient=patient, name_medicine=name,
                                date_of_taking_medicine=time, number_of_necessary_medicine=3,
                                number_of_medication_taken=rand)
            med.save()


class CompletedAnalyze(models.Model):
    patient = models.ForeignKey(Patient, verbose_name='Пациент', on_delete=models.CASCADE)
    name_analyze = models.CharField(verbose_name='Название анализа', max_length=60)
    date_of_completion = models.DateTimeField(verbose_name='Дата прохождения анализа')
    date_create = models.DateTimeField(verbose_name='Дата синхронизации', default=timezone.now())


class CompletedVisit(models.Model):
    patient = models.ForeignKey(Patient, verbose_name='Пациент', on_delete=models.CASCADE)
    name_doctor = models.CharField(verbose_name='Название доктора', max_length=60)
    date_of_completion = models.DateTimeField(verbose_name='Дата визита к врачу')
    date_create = models.DateTimeField(verbose_name='Дата синхронизации', default=timezone.now())


class CompletedProcedure(models.Model):
    patient = models.ForeignKey(Patient, verbose_name='Пациент', on_delete=models.CASCADE)
    name_procedure = models.CharField(verbose_name='Название процедуры', max_length=60)
    date_of_completion = models.DateTimeField(verbose_name='Дата выполнения процедуры')
    date_create = models.DateTimeField(verbose_name='Дата синхронизации', default=timezone.now())


class Test(models.Model):
    test = models.CharField(max_length=100)
