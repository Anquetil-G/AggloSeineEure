from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from ..forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserChangeFormAdmin, CustomUserCreationFormAdmin


User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def edit_account(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    user = get_object_or_404(User, pk=pk)
    form = CustomUserChangeForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'edit_account.html', {'form': form, 'user': user})



# def list_users(request):
#     users = User.objects.all()
#     return render(request, 'users/list.html', {'users': users})


# def create_user(request):
#     if request.method == 'POST':
#         form = CustomUserCreationFormAdmin(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('list_users')
#     else:
#         form = CustomUserCreationFormAdmin()
#     return render(request, 'users/create.html', {'form': form})


# def update_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     form = CustomUserChangeFormAdmin(request.POST or None, instance=user)
#     if form.is_valid():
#         form.save()
#         return redirect('list_users')
#     return render(request, 'users/edit.html', {'form': form, 'user': user})


# def delete_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         user.delete()
#         return redirect('list_users')
#     return render(request, 'users/delete.html', {'user': user})
