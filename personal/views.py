from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login as personal_login, logout as personal_logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.utils.decorators import method_decorator

from . import models
from . import forms
# Create your views here.


class login(View):
    template_name = 'personal/login.htm'

    context = {

    }
    grup = Group.objects.get(name='personal')

    def get(self, *args, **kwargs):

        # print(self.request.user)
        if self.request.user != None:

            user_grup = self.request.user.groups.all()
            if self.grup in user_grup:

                return redirect('personal:index')
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):

        # print(self.request.POST)
        username_input = self.request.POST['username']
        password_input = self.request.POST['password']

        user = authenticate(
            self.request, username=username_input, password=password_input)

        if user != None:
            user_grup = user.groups.all()
            if self.grup in user_grup:
                personal_login(self.request, user)
                return redirect('personal:index')
            else:
                self.context['error'] = 'Anda Tidak Punya Akses Kesini!'
                return render(self.request, self.template_name, self.context)

        else:
            self.context['error'] = 'Username Atau Password Salah'
            return render(self.request, self.template_name, self.context)

        # print(user_grup)


@permission_required('personal.add_about', login_url=None, raise_exception=True)
def index(request):
    # print(request.user.get_user_permissions())
    context = {

    }

    return render(request, 'personal/index.htm', context)


class logout(View):
    template_name = 'personal/login.htm'

    def get(self, *args, **kwargs):
        personal_logout(self.request)
        return render(self.request, self.template_name)


class personalView(View):

    template_name = 'personal/personal.htm'

    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):

        # print(self.request.user.groups.all())
        try:
            obj = models.personal.objects.get(user_id=self.request.user.id)
            # print(obj)
            data = obj.__dict__
            self.context['form'] = forms.PersonalForm(
                initial=data, instance=obj)
            self.context['button'] = 'Edit'

            return render(self.request, self.template_name, self.context)

        except models.personal.DoesNotExist:
            self.context['button'] = 'Tambah'
            self.context['form'] = forms.PersonalForm()
            return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        try:
            obj = models.personal.objects.get(user_id=self.request.user.id)
            self.form = forms.PersonalForm(
                self.request.POST, self.request.FILES, instance=obj)

        except models.personal.DoesNotExist:
            self.form = forms.PersonalForm(
                self.request.POST, self.request.FILES)

        if self.form.is_valid():
            save = self.form.save(commit=False)
            save.user = self.request.user
            save.save()
        return redirect('personal:personal')


class aboutView(View):
    template_name = 'personal/about.htm'
    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):
        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)

        try:
            obj = models.about.objects.get(personal_id=personal_id.id)
            data = obj.__dict__

            self.context['button'] = 'Edit'
            self.context['form'] = forms.AboutForm(initial=data, instance=obj)

        except models.about.DoesNotExist:

            self.context['button'] = 'Tambah'
            self.context['form'] = forms.AboutForm()

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)
        try:
            obj = models.about.objects.get(personal_id=personal_id.id)
            form = forms.AboutForm(self.request.POST, instance=obj)
            self.context['form'] = forms
        except models.about.DoesNotExist:
            form = forms.AboutForm(self.request.POST)
            self.context['form'] = forms

        if form.is_valid():
            save = form.save(commit=False)
            save.personal_id = personal_id.id
            save.save()

        return redirect('personal:about')


class skillView(View):
    template_name = 'personal/skills.htm'
    mode = None
    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):
        print(self.mode)
        if self.mode == 'delete':  # delete crud
            skillID = kwargs['id']
            models.skills.objects.filter(id=skillID).delete()
            return redirect('personal:skills')
        elif self.mode == 'update':  # update get data
            skillID = kwargs['id']
            try:
                obj = models.skills.objects.get(id=skillID)
                data = obj.__dict__
                # print(data)
                self.context['form'] = forms.SkillsForm(
                    instance=obj, initial=data)
                self.context['button'] = 'Edit'
            except models.skills.DoesNotExist:
                return redirect('personal:skills')
        else:
            self.context['form'] = forms.SkillsForm()
            self.context['button'] = 'Tambah'

        personal_id = models.personal.objects.get(user_id=self.request.user.id)
        listskill = models.skills.objects.filter(personal_id=personal_id.id)
        self.context['lists'] = listskill

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if self.mode == 'update':
            skillID = kwargs['id']
            obj = models.skills.objects.get(id=skillID)

            form = forms.SkillsForm(self.request.POST, instance=obj)
            self.context['form'] = form
            self.context['error'] = form.errors
        else:
            personal_id = models.personal.objects.get(
                user_id=self.request.user.id)
            form = forms.SkillsForm(self.request.POST)
            self.context['form'] = form
            self.context['error'] = form.errors

        if form.is_valid():
            if self.mode == 'update':
                form.save()
            else:
                save = form.save(commit=False)
                save.personal_id = personal_id.id
                save.save()
        if form.errors:
            return render(self.request, self.template_name, self.context)
        else:
            return redirect('personal:skills')


class resumeView(View):
    template_name = 'personal/resume.htm'
    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):
        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)
        try:
            obj = models.resume.objects.get(personal_id=personal_id.id)
            data = obj.__dict__
            self.context['form'] = forms.ResumeForm(initial=data, instance=obj)
            self.context['button'] = 'Edit'
        except models.resume.DoesNotExist:
            self.context['form'] = forms.ResumeForm()
            self.context['button'] = 'Tambah'
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)
        try:
            obj = models.resume.objects.get(personal_id=personal_id.id)
            form = forms.ResumeForm(self.request.POST, instance=obj)
            self.context['form'] = form
        except models.resume.DoesNotExist:
            form = forms.ResumeForm(self.request.POST)
            self.context['form'] = form

        if form.is_valid():
            save = form.save(commit=False)
            save.personal_id = personal_id.id
            save.save()
        return render(self.request, self.template_name, self.context)


class resumeSummaryView(View):
    template_name = 'personal/resume_summary.htm'
    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):
        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)
        resume_id = models.resume.objects.get(personal_id=personal_id.id)

        try:
            obj = models.resume_summary.objects.get(resume_id=resume_id.id)
            data = obj.__dict__
            self.context['form'] = forms.ResumeSummaryForm(
                initial=data, instance=obj)
            self.context['button'] = 'Edit'
        except models.resume_summary.DoesNotExist:
            self.context['form'] = forms.ResumeSummaryForm()
            self.context['button'] = 'Tambah'
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)
        resume_id = models.resume.objects.get(personal_id=personal_id.id)

        try:
            obj = models.resume_summary.objects.get(resume_id=resume_id.id)
            form = forms.ResumeSummaryForm(self.request.POST, instance=obj)
            self.context['form'] = form
        except models.resume_summary.DoesNotExist:
            form = forms.ResumeSummaryForm(self.request.POST)
            self.context['form'] = form

        if form.is_valid():

            save = form.save(commit=False)
            save.resume_id = resume_id.id
            save.save()
        return render(self.request, self.template_name, self.context)


class resumeEducationView(View):
    template_name = 'personal/resume_education.htm'
    mode = None
    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):
        if self.mode == 'update':
            try:
                obj = models.resume_education.objects.get(
                    id=kwargs['id'])
                data = obj.__dict__
                self.context['form'] = forms.ResumeEducationForm(
                    initial=data, instance=obj)
                self.context['button'] = 'Edit'
            except models.resume.DoesNotExist:
                return redirect('personal:resume_education')
        elif self.mode == 'delete':
            models.resume_education.objects.filter(id=kwargs['id']).delete()
            return redirect('personal:resume_education')
        else:
            self.context['form'] = forms.ResumeEducationForm()
            self.context['button'] = 'Tambah'

        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)
        resume_id = models.resume.objects.get(personal_id=personal_id.id)
        listskill = models.resume_education.objects.filter(
            resume_id=resume_id.id)
        self.context['lists'] = listskill
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):

        if self.mode == 'update':

            obj = models.resume_education.objects.get(id=kwargs['id'])
            form = forms.ResumeEducationForm(self.request.POST, instance=obj)
            self.context['form'] = form
        else:
            personal_id = models.personal.objects.get(
                user_id=self.request.user.id)
            resume_id = models.resume.objects.get(personal_id=personal_id.id)
            form = forms.ResumeEducationForm(self.request.POST)
            self.context['form'] = form

        if form.is_valid():
            if self.mode == 'update':
                form.save()
            else:
                save = form.save(commit=False)
                save.resume_id = resume_id.id
                save.save()
        return redirect('personal:resume_education')


class resumeExperienceView(View):
    template_name = 'personal/resume_experience.htm'
    mode = None
    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):
        if self.mode == 'update':
            try:
                obj = models.resume_experience.objects.get(
                    id=kwargs['id'])
                data = obj.__dict__
                self.context['form'] = forms.ResumeExperienceForm(
                    initial=data, instance=obj)
                self.context['button'] = 'Edit'
            except models.resume.DoesNotExist:
                return redirect('personal:resume_experience')
        elif self.mode == 'delete':
            models.resume_experience.objects.filter(id=kwargs['id']).delete()
            return redirect('personal:resume_experience')
        else:
            self.context['form'] = forms.ResumeExperienceForm()
            self.context['button'] = 'Tambah'

        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)
        resume_id = models.resume.objects.get(personal_id=personal_id.id)
        listskill = models.resume_experience.objects.filter(
            resume_id=resume_id.id)
        self.context['lists'] = listskill
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):

        if self.mode == 'update':

            obj = models.resume_experience.objects.get(id=kwargs['id'])
            form = forms.ResumeExperienceForm(self.request.POST, instance=obj)
            self.context['form'] = form
        else:
            personal_id = models.personal.objects.get(
                user_id=self.request.user.id)
            resume_id = models.resume.objects.get(personal_id=personal_id.id)
            form = forms.ResumeExperienceForm(self.request.POST)
            self.context['form'] = form

        if form.is_valid():
            if self.mode == 'update':
                form.save()
            else:
                save = form.save(commit=False)
                save.resume_id = resume_id.id
                save.save()
        return redirect('personal:resume_experience')


class servicesView(View):
    template_name = 'personal/services.htm'
    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):
        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)
        try:
            obj = models.services.objects.get(personal_id=personal_id.id)
            data = obj.__dict__
            self.context['form'] = forms.ServicesForm(
                initial=data, instance=obj)
            self.context['button'] = 'Edit'
        except models.services.DoesNotExist:
            self.context['form'] = forms.ServicesForm()
            self.context['button'] = 'Tambah'
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        personal_id = models.personal.objects.get(
            user_id=self.request.user.id)
        try:
            obj = models.services.objects.get(personal_id=personal_id.id)
            form = forms.ServicesForm(self.request.POST, instance=obj)
            self.context['form'] = form
        except models.services.DoesNotExist:
            form = forms.ServicesForm(self.request.POST)
            self.context['form'] = form

        if form.is_valid():
            save = form.save(commit=False)
            save.personal_id = personal_id.id
            save.save()
        return render(self.request, self.template_name, self.context)


class ServicesBodyView(View):
    template_name = 'personal/services_body.htm'
    mode = None
    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):
        print(self.mode)
        if self.mode == 'delete':  # delete crud
            servicesBodyID = kwargs['id']
            models.services_body.objects.filter(id=servicesBodyID).delete()
            return redirect('personal:services_body')
        elif self.mode == 'update':  # update get data
            servicesBodyID = kwargs['id']
            try:
                obj = models.services_body.objects.get(id=servicesBodyID)
                data = obj.__dict__
                # print(data)
                self.context['form'] = forms.ServicesBodyForm(
                    instance=obj, initial=data)
                self.context['button'] = 'Edit'
            except models.services_body.DoesNotExist:
                return redirect('personal:services_body')
        else:
            self.context['form'] = forms.ServicesBodyForm()
            self.context['button'] = 'Tambah'

        personal_id = models.personal.objects.get(user_id=self.request.user.id)
        services_id = models.services.objects.get(personal_id=personal_id.id)
        listservices = models.services_body.objects.filter(
            services_id=services_id.id)
        self.context['lists'] = listservices

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if self.mode == 'update':
            servicesBodyID = kwargs['id']
            obj = models.services_body.objects.get(id=servicesBodyID)

            form = forms.ServicesBodyForm(self.request.POST, instance=obj)
            self.context['form'] = form

        else:
            personal_id = models.personal.objects.get(
                user_id=self.request.user.id)
            services_id = models.services.objects.get(
                personal_id=personal_id.id)
            form = forms.ServicesBodyForm(self.request.POST)
            self.context['form'] = form

        if form.is_valid():
            if self.mode == 'update':
                form.save()
            else:
                save = form.save(commit=False)
                save.services_id = services_id.id
                save.save()

        return redirect('personal:services_body')


class TestimonialsView(View):
    template_name = 'personal/testimonials.htm'
    mode = None
    context = {

    }

    @method_decorator(user_passes_test(lambda user: Group.objects.get(name='personal') in user.groups.all()))
    def get(self, *args, **kwargs):
        print(self.mode)
        if self.mode == 'delete':  # delete crud
            testimonialID = kwargs['id']
            models.testimonials.objects.filter(id=testimonialID).delete()
            return redirect('personal:testimonials')
        elif self.mode == 'update':  # update get data
            testimonialID = kwargs['id']
            try:
                obj = models.testimonials.objects.get(id=testimonialID)
                data = obj.__dict__
                # print(data)
                self.context['form'] = forms.TestimonialsForm(
                    instance=obj, initial=data)
                self.context['button'] = 'Edit'
            except models.testimonials.DoesNotExist:
                return redirect('personal:testimonials')
        else:
            self.context['form'] = forms.TestimonialsForm()
            self.context['button'] = 'Tambah'

        personal_id = models.personal.objects.get(user_id=self.request.user.id)

        listtestimonials = models.testimonials.objects.filter(
            personal_id=personal_id.id)
        self.context['lists'] = listtestimonials

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if self.mode == 'update':
            testimonialID = kwargs['id']
            obj = models.testimonials.objects.get(id=testimonialID)

            form = forms.TestimonialsForm(self.request.POST, instance=obj)
            self.context['form'] = form

        else:
            personal_id = models.personal.objects.get(
                user_id=self.request.user.id)

            form = forms.TestimonialsForm(self.request.POST)
            self.context['form'] = form

        if form.is_valid():
            if self.mode == 'update':
                form.save()
                models.testimonials.save(kwargs['id'])

            else:
                save = form.save(commit=False)
                save.personal_id = personal_id.id
                save.save()

        return redirect('personal:testimonials')
