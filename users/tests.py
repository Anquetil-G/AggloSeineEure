from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Department, Commune, Contact
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class SetupMixin:
    def setUp(self):
        self.client = Client()

        self.department = Department.objects.create(name="Département Test")
        self.commune = Commune.objects.create(name="Commune Test", department=self.department)
        self.contact = Contact.objects.create(
            full_name="Jean Dupont",
            email="jean@test.com",
            phone_number="0600000000",
            commune=self.commune
        )

        self.global_admin = User.objects.create_user(username="global", password="test", rank="admin_global")
        self.department_admin = User.objects.create_user(username="deptadmin", password="test", rank="admin_department")
        self.commune_admin = User.objects.create_user(username="communeadmin", password="test", rank="admin_commune")
        self.user = User.objects.create_user(username="basicuser", password="test", rank="user")

        self.department_admin.administrated_departments.add(self.department)
        self.commune_admin.administrated_communes.add(self.commune)


class ViewTests(SetupMixin, TestCase):
    def test_view_contact_detail_authenticated(self):
        self.client.login(username="global", password="test")
        url = reverse("contact", kwargs={
            "pk": self.department.pk,
            "commune_pk": self.commune.pk,
            "contact_pk": self.contact.pk
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jean Dupont")

    def test_view_contact_detail_unauthenticated_redirect(self):
        url = reverse("contact", kwargs={
            "pk": self.department.pk,
            "commune_pk": self.commune.pk,
            "contact_pk": self.contact.pk
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_edit_contact_by_commune_admin(self):
        self.client.login(username="communeadmin", password="test")
        url = reverse("edit", kwargs={"model_name": "Contact", "pk": self.contact.pk})
        response = self.client.post(url, {
            "full_name": "Jean Modifié",
            "email": "modifie@test.com",
            "phone_number": "0606060606",
            "commune": self.commune.pk
        })
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.full_name, "Jean Modifié")

    def test_delete_contact_by_admin_global(self):
        self.client.login(username="global", password="test")
        url = reverse("delete", kwargs={"model_name": "Contact", "pk": self.contact.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())

    def test_delete_contact_by_unauthorized_user(self):
        self.client.login(username="basicuser", password="test")
        url = reverse("delete", kwargs={"model_name": "Contact", "pk": self.contact.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Contact.objects.filter(pk=self.contact.pk).exists())

    def test_upload_invalid_file_extension(self):
        self.client.login(username="global", password="test")
        url = reverse("create_with_parent", kwargs={
            "model_name": "Contact",
            "parent_pk": self.commune.pk,
            "parent_field": "commune",
            "parent_name": self.commune.name
        })
        invalid_file = SimpleUploadedFile("test.exe", b"fake content", content_type="application/octet-stream")
        response = self.client.post(url, {
            "full_name": "Fichier Test",
            "email": "fichier@test.com",
            "phone_number": "0101010101",
            "commune": self.commune.pk,
            "document": invalid_file
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seuls les fichiers PDF et Word")