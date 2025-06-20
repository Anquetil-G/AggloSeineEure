from django.shortcuts import render, redirect, get_object_or_404
from ..models import Contact, Department, Commune
from ..forms import ContactForm


def list_contacts_on_commune(request, pk=None, commune_pk=None):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        department = Department.objects.get(pk=pk)
        commune = Commune.objects.get(pk=commune_pk)
        contacts = Contact.objects.filter(commune=commune_pk)
        sorted_contacts = sorted(contacts, key=lambda c: c.full_name.lower())
        administrated_commune = request.user.administrated_communes.filter(id=commune_pk).exists()
        administrated_department = request.user.administrated_departments.filter(pk=pk).exists()

        context = {
            'department': department,
            'commune': commune,
            'contacts': sorted_contacts,
            'administrated_commune': administrated_commune,
            'administrated_department': administrated_department,
        }
        return render(request, 'commune_menu.html', context)


def list_one_contact(request, pk=None, commune_pk=None, contact_pk=None):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        department = Department.objects.get(pk=pk)
        contact = Contact.objects.get(pk=contact_pk)
        commune = Commune.objects.get(pk=commune_pk)
        administrated_commune = request.user.administrated_communes.filter(id=commune_pk).exists()
        administrated_department = request.user.administrated_departments.filter(pk=pk).exists()
        context = {
            'department': department,
            'commune': commune,
            'contact': contact,
            'administrated_commune': administrated_commune,
            'administrated_department': administrated_department,
        }
        return render(request, 'contact.html', context)



# def list_contacts(request):
#     contacts = Contact.objects.all()
#     return render(request, 'contacts/list.html', {'contacts': contacts})


# def create_contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('list_contacts')
#     else:
#         form = ContactForm()
#     return render(request, 'contacts/create.html', {'form': form})


# def update_contact(request, pk):
#     contact = get_object_or_404(Contact, pk=pk)
#     if request.method == 'POST':
#         form = ContactForm(request.POST, instance=contact)
#         if form.is_valid():
#             form.save()
#             return redirect('list_contacts')
#     else:
#         form = ContactForm(instance=contact)
#     return render(request, 'contacts/edit.html', {'form': form})


# def delete_contact(request, pk):
#     contact = get_object_or_404(Contact, pk=pk)
#     if request.method == 'POST':
#         contact.delete()
#         return redirect('list_contacts')
#     return render(request, 'contacts/delete.html', {'contact': contact})
