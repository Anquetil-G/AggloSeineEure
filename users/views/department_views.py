from django.shortcuts import render, redirect, get_object_or_404
from ..models import Department
from ..forms import DepartmentForm



# def list_departments(request):
#     departments = Department.objects.all()
#     return render(request, 'departments/list.html', {'departments': departments})


# def create_department(request):
#     if request.method == 'POST':
#         form = DepartmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('list_departments')
#     else:
#         form = DepartmentForm()
#     return render(request, 'departments/create.html', {'form': form})


# def update_department(request, pk):
#     department = get_object_or_404(Department, pk=pk)
#     if request.method == 'POST':
#         form = DepartmentForm(request.POST, instance=department)
#         if form.is_valid():
#             form.save()
#             return redirect('list_departments')
#     else:
#         form = DepartmentForm(instance=department)
#     return render(request, 'departments/edit.html', {'form': form})


# def delete_department(request, pk):
#     department = get_object_or_404(Department, pk=pk)
#     if request.method == 'POST':
#         department.delete()
#         return redirect('list_departments')
#     return render(request, 'departments/delete.html', {'department': department})
