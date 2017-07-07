from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import TakenMedicine, CompletedAnalyze, CompletedVisit, CompletedProcedure
from api.serializers import TakenMedicineSerializer, CompletedAnalysisSerializer, CompletedVisitSerializer, \
    CompletedProcedureSerializer, MedicineSerializer, AnalysisSerializer, ProcedureSerializer, VisitDoctorSerializer, \
    PatientSerializer, ResponseSerializer
from rest_framework import generics

# Medicine
from mydoctor.models import Medicine, Analysis, Procedure, VisitDoctor, Patient


class TakenMedicineMixin:
    queryset = TakenMedicine.objects.all()
    serializer_class = TakenMedicineSerializer


class TakenMedicinesCollection(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               TakenMedicineMixin,
                               generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Analyze
class CompletedAnalysisMixin:
    queryset = CompletedAnalyze.objects.all()
    serializer_class = CompletedAnalysisSerializer


class CompletedAnalysisCollection(mixins.ListModelMixin,
                                  mixins.CreateModelMixin,
                                  CompletedAnalysisMixin,
                                  generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Procedure
class CompletedProcedureSerializerMixin:
    queryset = CompletedProcedure.objects.all()
    serializer_class = CompletedProcedureSerializer


class CompletedProcedureSerializerCollection(mixins.ListModelMixin,
                                             mixins.CreateModelMixin,
                                             CompletedProcedureSerializerMixin,
                                             generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Visit
class CompletedVisitMixin:
    queryset = CompletedVisit.objects.all()
    serializer_class = CompletedVisitSerializer


class CompletedVisitCollection(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               CompletedVisitMixin,
                               generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Get data to app

# Medicine
class MedicineMixin:
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class MedicineCollection(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         MedicineMixin,
                         generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Analysis
class AnalysisMixin:
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer


class AnalysisCollection(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         AnalysisMixin,
                         generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Procedure
class ProcedureMixin:
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer


class ProcedureCollection(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          ProcedureMixin,
                          generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# VisitDoctor
class VisitDoctorMixin:
    queryset = VisitDoctor.objects.all()
    serializer_class = VisitDoctorSerializer


class VisitDoctorCollection(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            VisitDoctorMixin,
                            generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PatientCollection(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    model = Patient
    serializer_class = VisitDoctorSerializer

    def get_queryset(self):
        queryset = None
        email = self.request.query_params.get('email')
        password = self.request.query_params.get('password')

        if email | password:
            queryset = Patient.objects.filter(email=email, password=password)

        return queryset

@api_view(['POST'])
def patient_check(request):

    if request.method == 'POST':
        email = request.query_params.get("email")
        password = request.query_params.get('password')
        queryset = Patient.objects.filter(email=email)
        print(queryset)
        valid = "True"
        print(queryset.exists())
        if not queryset.exists():
            valid = "Не верный email"
        else:
            queryset = queryset.filter(password=password)
            if not queryset.exists():
                valid = "Не верный пароль"

        return Response(valid)
