from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.apps import apps
from django.forms import modelform_factory
from django.core.exceptions import PermissionDenied
from users.models import Department, Commune, Contact


def check_permissions(user, model_name, obj=None, post_data=None):
    model_name = model_name.lower()

    if user.rank == "admin_global":
        return True

    if model_name == "department":
        if obj:
            return obj in user.administrated_departments.all()
        elif post_data:
            dept = post_data.get('department')
            if isinstance(dept, Department):
                return dept in user.administrated_departments.all()
            return user.administrated_departments.filter(pk=dept).exists()

    elif model_name == "commune":
        if obj:
            return obj in user.administrated_communes.all()
        elif post_data:
            dept = post_data.get('department')
            if isinstance(dept, Department):
                return dept in user.administrated_departments.all()
            return user.administrated_departments.filter(pk=dept).exists()

    elif model_name == "contact":
        if obj:
            return obj.commune in user.administrated_communes.all()
        elif post_data:
            commune = post_data.get('commune')
            if isinstance(commune, Commune):
                return commune in user.administrated_communes.all()
            return user.administrated_communes.filter(pk=commune).exists()

    return False


def generic_edit(request, model_name, pk):
    if not request.user.is_authenticated:
        return redirect('home')

    Model = apps.get_model('users', model_name)
    obj = get_object_or_404(Model, pk=pk)

    if model_name.lower() != 'contact' and not check_permissions(request.user, model_name, obj=obj):
        raise PermissionDenied("Vous n'avez pas les droits pour modifier cet objet.")

    FormClass = modelform_factory(Model, fields='__all__')

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            if model_name.lower() == 'contact' and not check_permissions(request.user, model_name, obj=obj):
                cleaned = form.cleaned_data
                if (
                    cleaned.get('full_name') != obj.full_name or
                    cleaned.get('email') != obj.email or
                    cleaned.get('phone_number') != obj.phone_number
                ):
                    form.add_error(None, "Vous n'avez pas les droits pour modifier ces informations.")
                else:
                    form.save()
                    return redirect('home')
            else:
                form.save()
                return redirect('home')
    else:
        form = FormClass(instance=obj)

    if model_name.lower() == 'commune' and 'department' in form.fields:
        form.fields['department'].widget = forms.HiddenInput()
    elif model_name.lower() == 'contact':
        if 'commune' in form.fields:
            form.fields['commune'].widget = forms.HiddenInput()
        if not check_permissions(request.user, model_name, obj=obj):
            for field in ['full_name', 'email', 'phone_number']:
                if field in form.fields:
                    form.fields[field].widget = forms.HiddenInput()

    return render(request, 'edit.html', {
        'form': form,
        'object': obj,
        'model_name': model_name,
    })


def generic_delete(request, model_name, pk):
    if not request.user.is_authenticated:
        return redirect('home')

    Model = apps.get_model('users', model_name)
    obj = get_object_or_404(Model, pk=pk)

    if not check_permissions(request.user, model_name, obj=obj):
        raise PermissionDenied("Vous n'avez pas les droits pour supprimer cet objet.")

    if request.method == 'POST':
        obj.delete()
        return redirect('home')

    return render(request, 'delete.html', {'object': obj})


def generic_create(request, model_name, parent_pk=None, parent_field=None, parent_name=None):
    if not request.user.is_authenticated:
        return redirect('home')

    Model = apps.get_model('users', model_name)
    FormClass = modelform_factory(Model, fields='__all__')

    initial = {}
    if parent_pk and parent_field:
        initial[parent_field] = parent_pk

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, initial=initial)
    else:
        form = FormClass(initial=initial)

    if parent_field and parent_field in form.fields:
        form.fields[parent_field].widget = forms.HiddenInput()

    if request.method == 'POST' and form.is_valid():
        if not check_permissions(request.user, model_name, post_data=form.cleaned_data):
            raise PermissionDenied("Vous n'avez pas les droits pour créer cet objet.")
        form.save()
        return redirect('home')

    return render(request, 'create.html', {
        'form': form,
        'model_name': model_name,
        'object_name': parent_name,
    })
