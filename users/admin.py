from django.contrib import admin
from .models import CustomUser, Department, Commune, Contact
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
import csv
from django.http import HttpResponse


@admin.action(description="Exporter la base de donnée en CSV")
def export_hierarchical_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hierarchical_contacts.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Département',
        'Commune',
        'Nom du contact',
        'Téléphone',
        'Email',
        'Observation',
        'Rappel',
        'Document (URL)'
    ])

    departments = queryset.order_by('name')

    for department in departments:
        for commune in department.communes.all().order_by('name'):
            for contact in commune.contacts.all().order_by('full_name'):
                document_url = request.build_absolute_uri(contact.document.url) if contact.document else ''
                writer.writerow([
                    department.name,
                    commune.name,
                    contact.full_name,
                    contact.phone_number,
                    contact.email,
                    contact.observation or '',
                    contact.reminder or '',
                    document_url
                ])

    return response


class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': (
                'phone_number',
                'rank',
                'administrated_departments',
                'administrated_communes',
                'accessible_departments',
            ),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': (
                'phone_number',
                'rank',
                'administrated_departments',
                'administrated_communes',
                'accessible_departments',
            ),
        }),
    )
    filter_horizontal = (
        'administrated_departments',
        'administrated_communes',
        'accessible_departments',
    )


class DepartmentAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    actions = [export_hierarchical_csv]


class CommuneAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    actions = [export_hierarchical_csv]


class ContactAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    actions = [export_hierarchical_csv]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Commune, CommuneAdmin)
admin.site.register(Contact, ContactAdmin)

