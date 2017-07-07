from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/', views.LoginFormView.as_view(), name='login'),

    url(r'^patient/$', views.patient_list, name='patient_list'),
    url(r'^patient/create/$', views.patient_create, name='patient_create'),
    url(r'^patient/(?P<pk>\d+)/update/$', views.patient_update, name='patient_update'),
    url(r'^patient/(?P<pk>\d+)/delete/$', views.patient_delete, name='patient_delete'),

    url(r'^patient/(?P<pk>\d+)/recommendation/$', views.recommendation_list, name='recommendation_list'),
    url(r'^patient/(?P<pk>\d+)/recommendation/analysis/create/$', views.analysis_create, name='analysis_create'),
    url(r'^patient/(?P<pk>\d+)/recommendation/procedure/create/$', views.procedure_create, name='procedure_create'),
    url(r'^patient/(?P<pk>\d+)/recommendation/medicines/create/$', views.medicines_create, name='medicines_create'),
    url(r'^patient/(?P<pk>\d+)/recommendation/visit/create/$', views.visit_create, name='visit_create'),

    url(r'^patient/(?P<pk>\d+)/complet_recommendation/$', views.complet_recommendation_list, name='complet_recommendation_list'),

    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^registration/', views.UserFormView.as_view(), name='registration'),
    url(r'^ajax_dashboard_check/', views.ajax_dashboard_check, name='ajax_dashboard_check'),

]