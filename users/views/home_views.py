from django.shortcuts import render, redirect
from ..models import Department
from django.http import JsonResponse
from itertools import chain
from django.http import HttpResponse
from users.models import HistoricalDepartment, HistoricalCommune, HistoricalContact, HistoricalCustomUser
import csv


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    departments = Department.objects.all()

    if request.user.rank == 'admin_global':
        def annotate(entries):
            result = []
            for e in entries:
                try:
                    instance = e.instance
                    e.model_verbose_name = f"{instance._meta.verbose_name.title()} : {str(instance)}"
                except:
                    e.model_verbose_name = e._meta.verbose_name.title()

                if e.history_type == '+':
                    e.field_changes = ["Création"]
                elif e.history_type == '-':
                    e.field_changes = ["Suppression"]
                else:
                    try:
                        delta = e.diff_against(e.prev_record)
                        changes = [
                            f"{change.field} : « {change.old} » → « {change.new} »"
                            for change in delta.changes if change.field != "last_login"
                        ]
                        if changes:
                            e.field_changes = changes
                        else:
                            continue
                    except:
                        continue
                result.append(e)
            return result

            for e in entries:
                try:
                    instance = e.instance
                    e.model_verbose_name = f"{instance._meta.verbose_name.title()} : {str(instance)}"
                except:
                    e.model_verbose_name = e._meta.verbose_name.title()

                if e.history_type == '+':
                    e.field_changes = ["Création"]
                elif e.history_type == '-':
                    e.field_changes = ["Suppression"]
                else:
                    try:
                        delta = e.diff_against(e.prev_record)
                        e.field_changes = [
                            f"{change.field} : « {change.old} » → « {change.new} »"
                            for change in delta.changes if change.field != "last_login"
                        ]
                        if not e.field_changes:
                            e.field_changes = ["Aucun changement détecté"]
                    except:
                        e.field_changes = ["Impossible d’afficher les modifications"]
            return entries

        dept_history = annotate(HistoricalDepartment.objects.all())
        commune_history = annotate(HistoricalCommune.objects.all())
        contact_history = annotate(HistoricalContact.objects.all())
        user_history = annotate(HistoricalCustomUser.objects.all())

        all_history = sorted(
            chain(dept_history, commune_history, contact_history, user_history),
            key=lambda obj: obj.history_date,
            reverse=True
        )[:50]

        return render(request, 'home.html', {
            'history': all_history,
            'departments': departments
        })

    else:
        return render(request, 'home.html', {
            'history': [],
            'departments': departments
        })

