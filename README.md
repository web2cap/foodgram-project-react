## Product Assistant

### Project details:

SPA social network for storing and viewing recipes. Allows you to register, add and view recipes, add recipes to your favorites. Subscribe to the user. Add recipes to shopping lists and generate PDFs to buy the ingredients you need.

### Project composition:

The project includes:

1. Ready to use React frontend.
2. Django Rest Framework backend.
3. Database on Postgesql
4. NGINX


### Technical requirements of the project


```
gunicorn==20.0.4
Django==4.1
django-colorfield==0.7.2
django-extra-fields==3.0.2
django-filter==22.1
djangorestframework==3.13.1
djoser==2.1.0
html5lib==1.1 #
Pillow==9.2.0
psycopg2-binary==2.9.3
pyPdf==1.13
xhtml2pdf==0.2.8
```

### ENV structure

ST_SECRET_KEY # Django secret key
ST_ADMIN_LOGIN # Django superuser admin
ST_ADMIN_EMAIL # Django superuser email
ST_ADMIN_PASS # Django superuser password
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD # new postgres user password
DB_HOST=db
DB_PORT=5432
DB_USER=foodgram
DB_PASSWORD=foodgram

### How to start the project:

Install docker and docker compose
Clone the repository
Prepere .env file
Run infra/localstart.sh


### API description

A description of the project methods API is available at: /api/docs/

### Author:

* Pavel Koshelev (Teamlead)
