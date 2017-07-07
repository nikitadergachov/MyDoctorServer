from django.test import TestCase, Client
from django.urls import reverse

from mydoctor.forms import RegistrationForm, PatientForm, AnalysisForm, ProcedureForm
from mydoctor.models import MyUser
from mydoctor.views import LoginFormView


class UserTest(TestCase):

    def test_login_user(self):
        '''Проверка входа в систему'''
        c = Client()
        response = c.post(path='/login/', data={'email': 'pacient@mail.ru', 'password': '123456'})
        self.assertAlmostEquals(response.status_code, 200)

    def test_login_fake_user(self):
        '''Проверка входа в систему не существующего пользователя'''
        c = Client()
        response = c.post(path='/login/', data={'email': 'test@mail.ru', 'password': '123456'})
        self.assertAlmostEquals(response.status_code, 200)

    def test_patient_list(self):
        '''Вход в раздел список пациента и проверка вызванного шаблона'''
        c = Client()
        #user = MyUser.objects.get(email='pacient@mail.ru')
        response = c.get(path='/patient/')
        #response.user = user
        #self.assertTemplateUsed(response, 'mydoctor/recommendation/recommendation_list.html')


    def test_logout_user(self):
        '''Проверка выхода из системы в систему 
        и защита от входа не авторизированных пользователей'''

        c = Client()
        c.get(path='/logout/')
        response = c.get(path='/')
        self.assertAlmostEquals(response.status_code, 302)


    def test_registraion_not_valid(self):
        '''Проверка неправильно заполненной формы регистрации'''
        form_data = {'email': 'test@test', 'password': '123456', 'name':'Тест Кейсов Тест',
                     'phone_number': '+79780017814'}
        form = RegistrationForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_registraion_valid(self):
        '''Проверка неправильно заполненной формы регистрации'''
        form_data = {'email': 'test@mail.ru', 'password': '123456', 'name':'Тест Кейсов Тест',
                     'phone_number': '+79780017814'}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registraion_save(self):
        '''Проверка сохранения пользователя при регистрации'''
        form_data = {'email': 'test@mail.ru', 'password': '123456', 'name': 'Тест Кейсов Тест',
                     'phone_number': '+79780017814'}
        form = RegistrationForm(data=form_data)
        response = form.save()
        query = MyUser.objects.get(email='test@mail.ru')
        self.assertEquals(query.name, 'Тест Кейсов Тест')

    def test_add_pacient(self):
        '''Проверка правильно заполненной формы добавление пациента'''
        form_data = {'email': 'test@mail.ru', 'password': '123456', 'name':'Тест Кейсов Тест',
                     'phone_number': '+79780017814', 'insurance_number': '13214', 'DOB': '1985-11-24'}
        form = PatientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_analysis(self):
        '''Проверка неправильно заполненной формы регистрации'''
        form_data = {'name':'Тест анализ', 'description': '7 кабинет' }
        form = AnalysisForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_procedure(self):
        '''Проверка неправильно заполненной формы регистрации'''
        form_data = {'name': 'Тестовая процедура', 'description': '7 кабинет', 'number': '5'}
        form = ProcedureForm(data=form_data)
        self.assertTrue(form.is_valid())

