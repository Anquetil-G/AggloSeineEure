from django.urls import path
from django.contrib.auth import views as auth_views
from .views import user_views, department_views, commune_views, contact_views, home_views, global_views, admin_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', user_views.register, name='register'),
    path('edit-account/<int:pk>/', user_views.edit_account, name='edit_account'),
    path('search-commune/', commune_views.live_search_commune, name='live_search_commune'),

    path('departement/<int:pk>/', commune_views.list_communes_on_department, name='department_menu'),
    path('departement/<int:pk>/<int:commune_pk>/', contact_views.list_contacts_on_commune, name='commune_menu'),
    path('departement/<int:pk>/<int:commune_pk>/<int:contact_pk>', contact_views.list_one_contact, name='contact'),

    path('edit/<str:model_name>/<int:pk>/', global_views.generic_edit, name='edit'),
    path('delete/<str:model_name>/<int:pk>/', global_views.generic_delete, name='delete'),
    path('add/<str:model_name>/', global_views.generic_create, name='create'),
    path('add/<str:model_name>/<int:parent_pk>/<str:parent_field>/<str:parent_name>', global_views.generic_create, name='create_with_parent'),

    path('users/', admin_views.list_users, name='user_list'),
    path('search-user/', admin_views.live_search_user, name='live_search_user'),
    path('export-bdd/', admin_views.export_hierarchical_csv, name='export_bdd'),
    path('export-history/', admin_views.export_history, name='export_history'),



    # path('users/', user_views.list_users, name='list_users'),
    # path('users/create/', user_views.create_user, name='create_user'),
    # path('users/edit/<int:pk>/', user_views.update_user, name='edit_user'),
    # path('users/delete/<int:pk>/', user_views.delete_user, name='delete_user'),

    # path('departments/', department_views.list_departments, name='list_departments'),
    # path('departments/create/', department_views.create_department, name='create_department'),
    # path('departments/edit/<int:pk>/', department_views.update_department, name='edit_department'),
    # path('departments/delete/<int:pk>/', department_views.delete_department, name='delete_department'),

    # path('communes/', commune_views.list_communes, name='list_communes'),
    # path('communes/create/', commune_views.create_commune, name='create_commune'),
    # path('communes/edit/<int:pk>/', commune_views.update_commune, name='edit_commune'),
    # path('communes/delete/<int:pk>/', commune_views.delete_commune, name='delete_commune'),
    
    # path('contacts/', contact_views.list_contacts, name='list_contacts'),
    # path('contacts/create/', contact_views.create_contact, name='create_contact'),
    # path('contacts/edit/<int:pk>/', contact_views.update_contact, name='edit_contact'),
    # path('contacts/delete/<int:pk>/', contact_views.delete_contact, name='delete_contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)