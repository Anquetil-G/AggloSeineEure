from django.contrib import admin
from .models import CustomUser, Department, Commune, Contact
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
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


@admin.register(Department)
class DepartmentAdmin(SimpleHistoryAdmin):
    pass


@admin.register(Commune)
class CommuneAdmin(SimpleHistoryAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(SimpleHistoryAdmin):
    pass
