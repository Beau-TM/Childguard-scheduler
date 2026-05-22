Projectoverzicht
Childguard Scheduler is een webapplicatie gebouwd met Django.
Het doel van het project is om een planning‑ en bewakingssysteem te ontwikkelen voor scholen, waarbij gebruikers kunnen inloggen, planningen kunnen beheren en verschillende modules kunnen raadplegen.

De applicatie bestaat uit meerdere Django‑apps die elk een duidelijk afgebakende verantwoordelijkheid hebben.

Apps en hun functie
App	Functie
accounts	Login, logout, authenticatie
core	Homepagina’s, algemene views
planning	Planningen beheren en tonen
kalender	Kalenderfunctionaliteit
adminpaneel	Adminspecifieke pagina’s

Hoe start je het project op
1. Virtual environment activeren
Ga naar de juiste map:
cd Schoolbewaking

Activeer de venv:
..\venv\Scripts\activate

2. Server starten
python manage.py runserver

3. Problemen die ik ben tegengekomen
1. Python 3.14 was niet compatibel met Django
Ik had eerst Python 3.14 geïnstalleerd, maar Django ondersteunt deze versie nog niet.
Daardoor werkte:
python niet in de terminal
venv kon niet aangemaakt worden
manage.py kon niet uitgevoerd worden

Oplossing:  
Python 3.12 geïnstalleerd + “Add to PATH” aangevinkt.

2. Virtual environment werkte niet
Door de verkeerde Python‑versie was de venv beschadigd.

Oplossing:  
Nieuwe venv aangemaakt met Python 3.12.

3. Project werd vanuit de verkeerde map gestart
manage.py staat in:

Schoolbewaking/manage.py
maar ik zat in:

Childguard-schedular/
Oplossing:  
Naar de juiste map navigeren voor het starten van de server.

4. Huidige fout: URL‑configuratie
Django geeft:

ImproperlyConfigured: The included URLconf ... does not appear to have any patterns in it
Dit betekent dat er waarschijnlijk:
een fout zit in één van de andere urls.py bestanden
of een circular import
of een view die crasht tijdens import

Ik ben bezig met het controleren van alle URL‑modules om dit op te lossen.