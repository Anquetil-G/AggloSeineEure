from django.shortcuts import render, redirect, get_object_or_404
from ..models import Commune, Department
from ..forms import CommuneForm


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
