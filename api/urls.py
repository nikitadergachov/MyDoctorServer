from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'taken_medicine/$', views.TakenMedicinesCollection.as_view(), ),
    url(r'completed_analyze/$', views.CompletedAnalysisCollection.as_view(), ),
    url(r'completed_procedure/$', views.CompletedProcedureSerializerCollection.as_view(), ),
    url(r'completed_visit/$', views.CompletedVisitCollection.as_view(), ),
    url(r'medicine/$', views.MedicineCollection.as_view(), ),
    url(r'analysis/$', views.AnalysisCollection.as_view(), ),
    url(r'procedure/$', views.ProcedureCollection.as_view(), ),
    url(r'visit/$', views.VisitDoctorCollection.as_view(), ),
    url(r'patient_login/$', views.patient_check)
]