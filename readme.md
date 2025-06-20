# Projet de gestion de contacts

---

## 📦 Commandes DEV utiles

- python manage.py makemigrations           # Crée les fichiers de migration (à chaque modifs des models)
- python manage.py migrate                  # Applique les migrations (à chaque modifs des models)
- python manage.py createsuperuser          # Crée un admin pour accéder au /admin
- python manage.py runserver                # Lance le serveur en local
- python manage.py runserver 0.0.0.0:8000   # Lance le serveur en local + réseau local (accéssible sur mobile -> http://ipv4_pc:800 -> rajouter ip dans ALLOWED_HOSTS)
- python manage.py test                     # Lance les tests

---

## 📦 Stack technique

- Django (Python 3.10+)
- SQLite (par défaut)
- HTML / CSS pur
- django-simple-history

---

## 🧠 Fonctionnalités principales

- Création, édition, suppression de **contacts**
- Organisation des contacts par **communes**, elles-mêmes regroupées par **départements**
- Système d'**authentification** avec utilisateur personnalisé
- Permissions hiérarchiques : admin global, admin département, admin commune, utilisateur simple
- **Upload de documents** PDF ou Word pour chaque contact
- **Historique complet** des modifications pour chaque entité via Django Admin
- Interface d’administration via `/admin`

---

## 🗃️ Modèle de données

### Contact
- `full_name` (obligatoire)
- `phone_number` (obligatoire)
- `email` (obligatoire)
- `reminder` (facultatif, texte libre)
- `observation` (facultatif, texte libre)
- `document` (facultatif, fichier PDF ou Word)
- Lien vers une **commune**

### Commune
- `name`
- Lien vers un **département**

### Département
- `name`

### Custom User
- Hérite du modèle utilisateur Django
- Champs supplémentaires :
  - `phone_number`
  - `rank` (global_admin / department_admin / commune_admin / user)
  - `administrated_departments` (ManyToManyField)
  - `administrated_communes` (ManyToManyField)
  - `accessible_departments` (ManyToManyField)

---

## 🔐 Permissions

| Rôle                  | Lecture                                                                   | Création                                                     | Modification                                                                                 | Suppression                                                                                 |
|:----------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------|:---------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------|
| **Admin global**      | ✅ Tous                                                                  | ✅ Tous                                                      | ✅ Tous                                                                                     | ✅ Tous                                                                                     |
| **Admin département** | ✅ Ses accessible_departments & administrated_departments & leur contenu | ✅ Communes & contacts ( dans ses administrated_departments) | ✅ Communes & contacts (dans ses administrated_departments) & ses administrated_departments | ✅ Communes & contacts (dans ses administrated_departments) & ses administrated_departments |
| **Admin commune**     | ✅ Ses accessible_departments & administrated_communes & leur contenu    | ✅ Contacts (dans ses administrated_communes)                | ✅ Contacts (dans ses administrated_communes) & ses administrated_communes                  | ✅ Contacts (dans ses administrated_communes) & ses administrated_communes                  |
| **Utilisateur simple**| ✅ Ses accessible_departments & leur contenu                             | ❌                                                           | ☑️ Peut modifier observation, reminder et document des contacts                             | ❌                                                                                          |

---
