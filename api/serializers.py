from rest_framework import serializers

from api.models import TakenMedicine, CompletedAnalyze, CompletedVisit, CompletedProcedure, Test
from mydoctor.models import Medicine, Procedure, VisitDoctor, Analysis, Patient


class TakenMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenMedicine
        fields = ('patient', 'name_medicine', 'number_of_necessary_medicine',
                  'number_of_medication_taken', 'date_of_taking_medicine')


class CompletedAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedAnalyze
        fields = ('patient', 'name_analyze', 'date_of_completion')


class CompletedVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedVisit
        fields = ('patient', 'name_doctor', 'date_of_completion')


class CompletedProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedProcedure
        fields = ('patient', 'name_procedure', 'date_of_completion')


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ('id', 'name', 'type', 'method_reception', 'start_date', 'end_date',
                  'dosage', 'number_medicines', 'number_of_receptions_per_day',
                  'patient', 'description', 'after_meals')


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ('id', 'name', 'description', 'number', 'patient')


class VisitDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitDoctor
        fields = ('id', 'name_doctor', 'description', 'patient')


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ('id', 'name', 'description',)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        models = Patient
        fields = ('email', 'password')

class ResponseSerializer(serializers.Serializer):
    valid = serializers.CharField(required=False, allow_blank=True, max_length=100)
