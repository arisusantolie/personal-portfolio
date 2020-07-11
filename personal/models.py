from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.


class personal(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    birthday = models.DateField(auto_now_add=False, blank=True)
    nohp = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    alamat = models.TextField()
    degree = models.CharField(max_length=50)
    freelance_status = models.BooleanField(default=True)
    profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class about(models.Model):
    personal = models.OneToOneField(personal, on_delete=models.CASCADE)
    description = models.TextField()
    title = models.CharField(max_length=150)
    paragraph1 = models.TextField()
    paragraph2 = models.TextField()

    def __str__(self):
        return self.personal


def maxAbility(input):
    Ability = input
    if(Ability > 100):
        message = 'Tidak Boleh Lebih dari 100'
        raise ValidationError(message)


class skills(models.Model):

    personal = models.ForeignKey(personal, on_delete=models.CASCADE)
    skill = models.CharField(max_length=50)
    ability = models.IntegerField(validators=[maxAbility])

    def __str__(self):
        return self.skill


class resume(models.Model):

    personal = models.ForeignKey(personal, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.personal


class resume_summary(models.Model):

    resume = models.OneToOneField(resume, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.resume


class resume_education(models.Model):

    resume = models.ForeignKey(
        resume, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    period = models.CharField(max_length=50)
    alamat = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title


class resume_experience(models.Model):

    resume = models.ForeignKey(
        resume, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    period = models.CharField(max_length=50)
    alamat = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title


# class portfolio(models.Model):

#     def __str__(self):
#         return self.name

class services(models.Model):

    personal = models.OneToOneField(personal, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.personal


class services_body(models.Model):
    services = models.ForeignKey(services, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class testimonials(models.Model):

    personal = models.ForeignKey(personal, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        print(kwargs)
        # old = testimonials.objects.filter(id=id).first()
        # print(old)
        # if self.name.:
        #     self.position = 'hahaha'
        # else:
        super().save(*args, **kwargs)  # Call the "real" save() method.


class contact(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name
