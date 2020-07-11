from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test
from . import views

app_name = 'personal'

urlpatterns = [
    path('', views.login.as_view(), name='login'),
    path('dashboard/', views.index, name="index"),
    path('logout/', login_required(views.logout.as_view()), name='logout'),
    path('personal/', views.personalView.as_view(), name='personal'),
    path('about/', views.aboutView.as_view(), name='about'),
    path('skills/', views.skillView.as_view(), name='skills'),
    path('skills/<id>/update',
         views.skillView.as_view(mode='update'), name='skillUPDATE'),
    path('skills/<id>/delete',
         views.skillView.as_view(mode='delete'), name='skillDELETE'),
    path('resume/', views.resumeView.as_view(), name='resume'),
    path('resume-summary/', views.resumeSummaryView.as_view(), name='resume_summary'),
    path('resume-education', views.resumeEducationView.as_view(),
         name='resume_education'),
    path('resume-education/<id>/update',
         views.resumeEducationView.as_view(mode='update'), name='resume_education_update'),
    path('resume-education/<id>/delete',
         views.resumeEducationView.as_view(mode='delete'), name='resume_education_delete'),
    path('resume-experience', views.resumeExperienceView.as_view(),
         name='resume_experience'),
    path('resume-experience/<id>/update',
         views.resumeExperienceView.as_view(mode='update'), name='resume_experience_update'),
    path('resume-experience/<id>/delete',
         views.resumeExperienceView.as_view(mode='delete'), name='resume_experience_delete'),
    path('services/', views.servicesView.as_view(), name='services'),
    path('servies-body/', views.ServicesBodyView.as_view(), name='services_body'),
    path('servies-body/<id>/update',
         views.ServicesBodyView.as_view(mode='update'), name='services_body_update'),
    path('servies-body/<id>/delete',
         views.ServicesBodyView.as_view(mode='delete'), name='services_body_delete'),
    path('testimonials/', views.TestimonialsView.as_view(), name='testimonials'),
    path('testimonials/<id>/update',
         views.TestimonialsView.as_view(mode='update'), name='testimonials_update'),
    path('testimonials/<id>/delete',
         views.TestimonialsView.as_view(mode='delete'), name='testimonials_delete'),

]
