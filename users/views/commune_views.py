from django.shortcuts import render, redirect, get_object_or_404
from ..models import Commune, Department
from ..forms import CommuneForm
from django.http import JsonResponse
from django.db import models


def list_communes_on_department(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        communes = Commune.objects.filter(department_id=pk)
        administrated_communes = request.user.administrated_communes.filter(department_id=pk)
        administrated_department = request.user.administrated_departments.filter(pk=pk).exists()
        department = Department.objects.get(pk=pk)  

        context = {
            'department': department,
            'communes': communes,
            'administrated_communes': administrated_communes,
            'administrated_department': administrated_department,
        }
        return render(request, 'department_menu.html', context)


def live_search_commune(request):
    query = request.GET.get('q', '').strip()
    user = request.user
    results = []

    if not query:
        return JsonResponse({'results': []})

    communes_qs = Commune.objects.none()

    if user.rank == 'admin_global':
        communes_qs = Commune.objects.filter(name__icontains=query)

    elif user.rank == 'admin_department':
        communes_qs = Commune.objects.filter(
            name__icontains=query,
            department__in=user.administrated_departments.all() | user.accessible_departments.all()
        )

    elif user.rank == 'admin_commune':
        communes_qs = Commune.objects.filter(
            name__icontains=query
        ).filter(
            models.Q(pk__in=user.administrated_communes.all()) |
            models.Q(department__in=user.accessible_departments.all())
        )

    elif user.rank == 'user':
        communes_qs = Commune.objects.filter(
            name__icontains=query,
            department__in=user.accessible_departments.all()
        )

    for commune in communes_qs.select_related('department').distinct()[:10]:
        is_admin = False
        if user.rank == 'admin_global':
            is_admin = True
        elif user.rank == 'admin_department' and commune.department in user.administrated_departments.all():
            is_admin = True
        elif user.rank == 'admin_commune' and commune in user.administrated_communes.all():
            is_admin = True

        results.append({
            'name': commune.name,
            'id': commune.id,
            'department': {
                'name': commune.department.name,
                'id': commune.department.id
            },
            'is_admin': is_admin,
        })

    return JsonResponse({'results': results})



# def list_communes(request):
#     communes = Commune.objects.all()
#     return render(request, 'communes/list.html', {'communes': communes})


# def create_commune(request):
#     if request.method == 'POST':
#         form = CommuneForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('list_communes')
#     else:
#         form = CommuneForm()
#     return render(request, 'communes/create.html', {'form': form})


# def update_commune(request, pk):
#     commune = get_object_or_404(Commune, pk=pk)
#     if request.method == 'POST':
#         form = CommuneForm(request.POST, instance=commune)
#         if form.is_valid():
#             form.save()
#             return redirect('list_communes')
#     else:
#         form = CommuneForm(instance=commune)
#     return render(request, 'communes/edit.html', {'form': form})


# def delete_commune(request, pk):
#     commune = get_object_or_404(Commune, pk=pk)
#     if request.method == 'POST':
#         commune.delete()
#         return redirect('list_communes')
#     return render(request, 'communes/delete.html', {'commune': commune})
