from django.contrib import auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import context
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView

from api.models import TakenMedicine, CompletedAnalyze, CompletedVisit, CompletedProcedure
from mydoctor import forms
from mydoctor.backend import CustomUserAuth
from mydoctor.forms import RegistrationForm, LoginForm, PatientForm, ProcedureForm, MedicinesForm, \
    VisitDoctorForm, AnalysisForm
from mydoctor.models import MyUser, Patient, Analysis, VisitDoctor, Medicine, Procedure
from django_ajax.decorators import ajax


@login_required(login_url='login')
def dashboard(request):
    template = 'mydoctor/main_dashboard.html'
    users = MyUser.objects.all()
    patients = Patient.objects.filter(doctor=request.user)

    return render(request, template, {'name': request.user.get_full_name(), 'users': users, 'patients': patients})


@login_required(redirect_field_name='login')
def logout_view(request):
    logout(request)
    return redirect('login')


# Crud patuents
@login_required(redirect_field_name='login')
def patient_list(request):
    patients = Patient.objects.filter(doctor=request.user)
    return render(request, 'mydoctor/pacient/patient_list.html',
                  {'patients': patients, 'name': request.user.get_full_name()})


def save_patient_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():

            patient = form.save(commit=False)
            patient.doctor = request.user
            patient.save()

            data['form_is_valid'] = True
            patients = Patient.objects.all()
            data['html_patients_list'] = render_to_string('mydoctor/pacient/includes/tbody.html',
                                                          {'patients': patients}, request=request)
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
    else:
        form = PatientForm()
    return save_patient_form(request, form, 'mydoctor/pacient/includes/create.html')


def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
    else:
        form = PatientForm(instance=patient)

    return save_patient_form(request, form, 'mydoctor/pacient/includes/update.html')


def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    print('this')
    print(pk)
    print(patient.name)
    data = dict()
    if request.method == 'POST':
        patient.delete()
        data['form_is_valid'] = True
        patients = Patient.objects.all()
        data['html_patients_list'] = render_to_string('mydoctor/pacient/includes/tbody.html', {'patients': patients})
    else:
        context = {'patient': patient}
        data['html_form'] = render_to_string('mydoctor/pacient/includes/delete.html', context, request=request)
    return JsonResponse(data)


# Recomendation
def recommendation_list(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    patients = Patient.objects.filter(doctor=request.user)

    analysis = Analysis.objects.filter(patient=patient)
    visits_doctor = VisitDoctor.objects.filter(patient=patient)
    medicines = Medicine.objects.filter(patient=patient)
    procedures = Procedure.objects.filter(patient=patient)

    # forms
    analysis_form = AnalysisForm
    procedure_form = ProcedureForm
    medicine_form = MedicinesForm
    visit_form = VisitDoctorForm

    template = 'mydoctor/recommendation/recommendation_list.html'
    return render(request, template,
                  {'analysis': analysis,
                   'visits_doctor': visits_doctor,
                   'medicines': medicines,
                   'procedures': procedures,
                   'name': request.user.get_full_name(),
                   'patient': patient,

                   'analysis_form': analysis_form,
                   'procedure_form': procedure_form,
                   'medicine_form': medicine_form,
                   'visit_form': visit_form,

                   'patients': patients})


def analysis_create(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.patient = patient
            analysis.save()
    return redirect('recommendation_list', pk)


def procedure_create(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = ProcedureForm(request.POST)
        if form.is_valid():
            procedure = form.save(commit=False)
            procedure.patient = patient
            procedure.save()
    return redirect('recommendation_list', pk)


def visit_create(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = VisitDoctorForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = patient
            visit.save()
    return redirect('recommendation_list', pk)


def medicines_create(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = MedicinesForm(request.POST)
        if form.is_valid():
            medicines = form.save(commit=False)
            medicines.patient = patient
            medicines.save()
    return redirect('recommendation_list', pk)


class LoginFormView(View):
    form_class = LoginForm
    template = 'mydoctor/login.html'

    def get(self, request: object) -> object:
        print(request.user)
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=email, password=password)
            print(user)
            print('this')
            if user is not None:
                print('login')
                print(user)
                print(request.POST)
                auth.login(request, user)
                return redirect('dashboard')

        return render(request, self.template, {'form': form})


class UserFormView(View):
    form_class = RegistrationForm
    template = 'mydoctor/registration.html'

    def get(self, request: object) -> object:
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            email = form.cleaned_data['email']
            print('key' + email)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

        return render(request, self.template, {'form': form})


@ajax
def ajax_dashboard_check(request):
    _id = request.POST.get('id')
    _name = request.POST.get('name')
    _checked = request.POST.get('checked')
    if (_checked == 'true'):
        _checked = True
    else:
        _checked = False

    user = MyUser.objects.get(id=_id)
    print(user)
    print(_id)
    print(_name)
    print(_checked)
    if _name == 'is_admin':
        user.is_admin = _checked
    if _name == 'is_active':
        user.is_active = _checked

    user.save()


# Completed recomendation
def complet_recommendation_list(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patients = Patient.objects.filter(doctor=request.user)

    # TakenMedicine.generate_date()


    analysis = CompletedAnalyze.objects.filter(patient=patient)
    visits_doctor = CompletedVisit.objects.filter(patient=patient)
    medicines = TakenMedicine.objects.filter(patient=patient)

    count_taken = 0
    count = 0
    number = []
    for item in medicines:
        count_taken += item.number_of_medication_taken
        count += item.number_of_necessary_medicine



    procedures = CompletedProcedure.objects.filter(patient=patient)

    template = 'mydoctor/completed_recomendation/completed_recomendation.html'
    return render(request, template,
                  {'analysis': analysis,
                   'visits_doctor': visits_doctor,
                   'medicines': medicines,
                   'procedures': procedures,
                   'name': request.user.get_full_name(),
                   'patient': patient,
                   'patients': patients,
                   'count': count,
                   'count_taken': count_taken})
