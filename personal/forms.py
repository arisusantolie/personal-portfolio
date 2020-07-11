from django import forms
from . import models


class PersonalForm(forms.ModelForm):

    class Meta:
        model = models.personal
        fields = ("name", "birthday", "nohp", "email", "website", "alamat",
                  "degree", "freelance_status", "profile_pic")


class AboutForm(forms.ModelForm):

    class Meta:
        model = models.about
        fields = ('description', 'title', 'paragraph1', 'paragraph2')
        labels = {
            'description': 'Deskripsi Diri'
        }


class SkillsForm(forms.ModelForm):

    class Meta:
        model = models.skills
        fields = ("skill", "ability")
        widgets = {
            'skill': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nama skill'
                }

            ),
            'ability': forms.NumberInput(

                attrs={
                    'class': 'form-control ',
                    'placeholder': 'Persentasi Skill'
                }

            )
        }


class ResumeForm(forms.ModelForm):

    class Meta:
        model = models.resume
        fields = ('description',)


class ResumeSummaryForm(forms.ModelForm):

    class Meta:
        model = models.resume_summary
        fields = ("description",)


class ResumeEducationForm(forms.ModelForm):

    class Meta:
        model = models.resume_education
        fields = ("title", "period", "alamat", "description")


class ResumeExperienceForm(forms.ModelForm):

    class Meta:
        model = models.resume_experience
        fields = ("title", "period", "alamat", "description")


class ServicesForm(forms.ModelForm):

    class Meta:
        model = models.services
        fields = ('description',)


class ServicesBodyForm(forms.ModelForm):

    class Meta:
        model = models.services_body
        fields = ("name", 'icon', 'description')


class TestimonialsForm(forms.ModelForm):

    class Meta:
        model = models.testimonials
        fields = ("name", "position", "description")
