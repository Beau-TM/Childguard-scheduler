# Childguard Scheduler – Django

Beau Ingang en Lenn Dehert

Childguard-scheduler is een webapplicatie die speelplaatsbewakingen in scholen automatisch en eerlijk verdeelt onder leerkrachten. Het systeem houdt rekening met werkpercentages (voltijds/halftijds), afwezigheden, weekends en speciale dagen zoals feestdagen of studiedagen. Leerkrachten en directie kunnen inloggen via een beveiligd platform met elk hun eigen rechten en overzichten.

## Projectstructuur

```
childguard_v3/
├── config/                  # Django project configuratie
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── childguard/              # Hoofd Django app
│   ├── models.py            # Database modellen
│   ├── views.py             # View logica
│   ├── forms.py             # Django formulieren
│   ├── admin.py             # Admin configuratie
│   ├── urls.py              # URL routes
│   ├── context_processors.py
│   ├── templates/
│   │   ├── childguard/      # App templates
│   │   └── registration/    # Login template
│   └── static/
│       └── childguard/
│           └── css/main.css # Alle styling
├── manage.py
├── requirements.txt
└── create_demo_data.py      # Demo data script
```

## Installatie & Opstarten

```bash
# 1. Installeer Django
pip install -r requirements.txt

# 2. Database aanmaken
python manage.py migrate

# 3. Demo data aanmaken (gebruikers + leerkrachten)
python create_demo_data.py

# 4. Development server starten
python manage.py runserver
```

Ga dan naar: http://127.0.0.1:8000/

## Demo Accounts

| Gebruiker  | Wachtwoord   | Rol              |
|------------|--------------|------------------|
| admin      | admin123     | Systeembeheerder |
| directie   | directie123  | Directie         |
| teacher1   | teacher123   | Anna Janssens    |
| teacher2   | teacher123   | Pieter De Vries  |
| teacher3   | teacher123   | Sophie Peeters   |

*Leerkrachten moeten bij eerste login een nieuw wachtwoord kiezen.*

## Functionaliteiten

- **Login / Uitloggen** – rolgebaseerde toegang (admin, directie, leerkracht)
- **Dashboard** – statistieken en snelle acties
- **Leerkrachten beheren** – toevoegen, bewerken, verwijderen
- **Planning Genereren** – automatische eerlijke verdeling op basis van werkpercentage
- **Planning Geschiedenis** – alle gegenereerde maandplanningen
- **Gezamenlijke Kalender** – maandoverzicht met alle bewakingen
- **Leerkracht Kalender** – persoonlijke kalender per leerkracht
- **Afmeldingen** – indienen en beheren van afmeldingen
- **Speciale Dagen** – vakantiedagen, uitstappen, studiedagen
- **Mijn Lesuren** – overzicht per leerkracht
- **School Overzicht** – statistieken per leerkracht (admin)

## Productie

Voor productie: zet `DEBUG = False` in `settings.py`, gebruik een echte
database (PostgreSQL), en stel een sterke `SECRET_KEY` in via een
omgevingsvariabele.
