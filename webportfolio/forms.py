from django import forms
from personal.models import contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = contact
        fields = ('__all__')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'data-rule': 'minlen:4',
                    'data-msg': 'Please enter at least 4 chars'
                }),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'data-rule': 'email',
                    'data-msg': 'Please enter a valid email'
                }),
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'data-rule': 'minlen:8',
                    'data-msg': 'Please enter at least 8 chars of subject'
                }),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': "10",
                    'data-rule': 'required',
                    'data-msg': 'Please write something for us'
                }),


        }
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'subject': 'Subject',
            'message': 'Message'
        }
