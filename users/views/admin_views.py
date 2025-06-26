from django.shortcuts import render
from users.models import Department, CustomUser
from django.http import HttpResponse
from users.models import HistoricalDepartment, HistoricalCommune, HistoricalContact, HistoricalCustomUser
import csv
from django.http import JsonResponse
from itertools import chain



def list_users(request):
    users = CustomUser.objects.all()
    return render(request, 'users_list.html', {'users': users})


def export_hierarchical_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export_bdd.csv"'

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

    departments = Department.objects.order_by('name')

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
                    document_url or ''
                ])

    return response


def live_search_user(request):
    user = request.user
    if user.rank == 'admin_global':
        query = request.GET.get('q', '').strip()
        results = []

        if query:
            matched_users = CustomUser.objects.filter(username__icontains=query)[:10]
            for matched_user in matched_users:
                results.append({
                    'username': matched_user.username,
                    'id': matched_user.id,
                })

        return JsonResponse({'results': results})
    else:
        return JsonResponse({'results': []})


def export_history(request):
    if not request.user.is_authenticated or request.user.rank != 'admin_global':
        return HttpResponse(status=403)

    IGNORED_FIELDS = ['last_login']

    dept_history = HistoricalDepartment.objects.all()
    commune_history = HistoricalCommune.objects.all()
    contact_history = HistoricalContact.objects.all()
    user_history = HistoricalCustomUser.objects.all()

    all_history = sorted(
        chain(dept_history, commune_history, contact_history, user_history),
        key=lambda obj: obj.history_date,
        reverse=True
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historique_complet.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Utilisateur', 'Objet', 'Type d\'action', 'Modifications'])

    for entry in all_history:
        username = entry.history_user.username if entry.history_user else "Inconnu"

        try:
            instance = entry.instance
            obj_name = f"{instance._meta.verbose_name.title()} : {str(instance)}"
        except:
            obj_name = entry._meta.verbose_name.title()

        action_type = {
            '+': 'Création',
            '~': 'Modification',
            '-': 'Suppression'
        }.get(entry.history_type, 'Inconnu')

        # Traitement des changements
        if entry.history_type == '+':
            changes = "Création sans détails"
        elif entry.history_type == '-':
            changes = "Suppression sans détails"
        else:
            try:
                delta = entry.diff_against(entry.prev_record)
                changes_list = [
                    f"{change.field} : {change.old} → {change.new}"
                    for change in delta.changes
                    if change.field not in IGNORED_FIELDS
                ]
                if not changes_list:
                    continue
                changes = "; ".join(changes_list)
            except:
                continue

        writer.writerow([
            entry.history_date.strftime("%d/%m/%Y %H:%M"),
            username,
            obj_name,
            action_type,
            changes
        ])

    return response

