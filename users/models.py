from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)

    RANK_CHOICES = [
        ('admin_global', 'Admin Global'),
        ('admin_department', 'Admin Département'),
        ('admin_commune', 'Admin Commune'),
        ('user', 'Utilisateur'),
    ]
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, default='user')

    administrated_departments = models.ManyToManyField(
        'users.Department',
        blank=True,
        related_name='admins'
    )

    administrated_communes = models.ManyToManyField(
        'users.Commune',
        blank=True,
        related_name='admins'
    )

    accessible_departments = models.ManyToManyField(
        'users.Department',
        blank=True,
        related_name='accessible_users'
    )

    def __str__(self):
        return self.username


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    history = HistoricalRecords()

    def clean(self):
        super().clean()
        if Department.objects.filter(name__iexact=self.name).exclude(pk=self.pk).exists():
            raise ValidationError({'name': "Ce nom existe déjà"})

    def __str__(self):
        return self.name


class Commune(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="communes")
    history = HistoricalRecords()

    def clean(self):
        super().clean()
        if Commune.objects.filter(name__iexact=self.name).exclude(pk=self.pk).exists():
            raise ValidationError({'name': "Ce nom existe déjà"})

    def __str__(self):
        return f"{self.name} ({self.department.name})"


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Seuls les fichiers PDF et Word (.doc, .docx) sont autorisés.')


class Contact(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    observation = models.TextField(blank=True)
    reminder = models.TextField(blank=True)
    document = models.FileField(upload_to='documents/', validators=[validate_file_extension], blank=True, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name="contacts")

    def clean(self):
        super().clean()
        if Contact.objects.filter(full_name__iexact=self.full_name).exclude(pk=self.pk).exists():
            raise ValidationError({'full_name': "Ce nom existe déjà"})

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.full_name} ({self.commune.name})"
