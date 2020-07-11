from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from personal.models import *
from datetime import date
from django.views import View
from . import forms
from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.contrib import messages
import math
# def index(request):

#     return render(request, 'index.htm', context)


class IndexView(View):

    template_name = "index.htm"
    # print(personal.objects.get(id=3))
    context = {

    }
    pro = personal.objects.get(id=3)
    yearnow = date.today()
    age = yearnow.year - pro.birthday.year

    def get(self, *args, **kwargs):

        personal_id = personal.objects.get(id=3)
        self.context["profile"] = personal_id
        self.context['age'] = self.age
        self.context['about'] = about.objects.get(personal_id=personal_id.id)
        countskill = skills.objects.filter(personal_id=personal_id.id).count()
        avgSkill = math.ceil(countskill/2)
        self.context['skills1'] = skills.objects.filter(
            personal_id=personal_id.id)[0:avgSkill]
        self.context['skills2'] = skills.objects.filter(
            personal_id=personal_id.id)[avgSkill:]

        resume_id = resume.objects.get(personal_id=personal_id.id)
        self.context['resume_desc'] = resume_id
        self.context['resume_summary'] = resume_summary.objects.get(
            resume_id=resume_id.id)
        self.context['resume_education'] = resume_education.objects.filter(
            resume_id=resume_id.id).order_by('-period')  # -  untuk desc
        self.context['resume_experience'] = resume_experience.objects.filter(
            resume_id=resume_id.id).order_by('-period')
        services_id = services.objects.get(personal_id=personal_id.id)
        self.context['services_desc'] = services_id
        self.context['services_body'] = services_body.objects.filter(
            services_id=services_id)

        self.context['testimonials'] = testimonials.objects.filter(
            personal_id=personal_id.id)
        self.context['form'] = forms.ContactForm()
        self.context['statusmail'] = 'None'
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        subject = self.request.POST['subject']
        from_email = 'admin@arisusantolie.com'

        message = 'Nama : {}<br>Email : {}<br>Pesan : {}\n'.format(
            self.request.POST['name'], self.request.POST['email'], self.request.POST['message'])

        if subject and message and from_email:
            self.context['form'] = forms.ContactForm()
            try:
                msg = EmailMultiAlternatives(
                    subject, message, from_email, ['arisusantolie12@gmail.com'])
                # send_mail(subject, message, from_email, ['admin@example.com'])
                msg.attach_alternative(message, "text/html")
                msg.send()
                messages.success(
                    self.request, 'Your message has been sent. Thank you!')
            except BadHeaderError:
                messages.error(
                    self.request, 'Your Failed To Sended. Please Try Again!')

            return redirect('index')


# class IndexView(TemplateView):

#     template_name = "index.htm"
#     # print(personal.objects.get(id=3))
#     pro = personal.objects.get(id=3)
#     yearnow = date.today()
#     age = yearnow.year - pro.birthday.year

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         personal_id = personal.objects.get(id=3)
#         context["profile"] = personal_id
#         context['age'] = self.age
#         context['about'] = about.objects.get(personal_id=personal_id.id)
#         countskill = skills.objects.filter(personal_id=personal_id.id).count()
#         avgSkill = math.ceil(countskill/2)
#         context['skills1'] = skills.objects.filter(
#             personal_id=personal_id.id)[0:avgSkill]
#         context['skills2'] = skills.objects.filter(
#             personal_id=personal_id.id)[avgSkill:]

#         resume_id = resume.objects.get(personal_id=personal_id.id)
#         context['resume_desc'] = resume_id
#         context['resume_summary'] = resume_summary.objects.get(
#             resume_id=resume_id.id)
#         context['resume_education'] = resume_education.objects.filter(
#             resume_id=resume_id.id).order_by('-period')  # -  untuk desc
#         context['resume_experience'] = resume_experience.objects.filter(
#             resume_id=resume_id.id).order_by('-period')
#         services_id = services.objects.get(personal_id=personal_id.id)
#         context['services_desc'] = services_id
#         context['services_body'] = services_body.objects.filter(
#             services_id=services_id)

#         context['testimonials'] = testimonials.objects.filter(
#             personal_id=personal_id.id)

#         return context
