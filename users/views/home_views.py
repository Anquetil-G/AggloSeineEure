from django.shortcuts import render
from ..models import Department

def home(request):
    departments = Department.objects.all()
    return render(request, 'home.html', {'departments': departments})