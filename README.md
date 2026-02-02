## Entwicklungsumgebung:

poetry installieren (z.B mit pipx). Folgendn Befehl ausführen, um die Projektabhängigkeiten zu installieren:

```
poetry install
```

Auf Debian/Ubuntu kann `psycopg2` mit dem Befehl `apt install python3-psycopg2` installiert werden. Falls eine Installation über PyPI gewünscht ist, kann dieses beispielsweise mit diesem Befehl passieren:

```
poetry run pip install psycopg2-binary
```

Die Settings-Variablen können als environment variables, beispielsweise in `.env.local` (während der Entwicklung) oder in `.env` (während der Produktion), gesetzt werden. Als Beispiel für `.env.local`:

```
ROTEBEETE_SECRET_KEY=VerySecretKey
ROTEBEETE_DEBUG=True
ROTEBEETE_ALLOWED_HOSTS=127.0.0.1
ROTEBEETE_DATABASE_URL=postgres://<user>:<password>@localhost:5432/<db>
ROTEBEETE_EMAIL_HOST_PASSWORD=VerySecretPassword
```

Django-Management-Befehle:

```
poetry run python manage.py migrate
poetry run python manage.py collectstatic
poetry run python manage.py createsuperuser
poetry run python manage.py create_member_for_superusers
poetry run python manage.py runserver
```

Test-Dateien (s. https://juntagrico.readthedocs.io/en/latest/intro/installation.html)

```
poetry run python -m manage generate_testdata
poetry run python -m manage generate_testdata_advanced
```

## Biterrunden

Wir gehen zurzeit davon aus, dass jedes Mitglied nur eine einzige Mitgliedschaft hat. Falls dieses Verhalten sich ändern soll, müssen `biddings.views._UserSubscriptionMixin._get_subscription()`, `biddings.templatetags.get_bid()` und `biddings.templates.biddings.biddinground_list.html` entsprechend aktualisiert werden.

## Dokumentation von Anpassungen

_zur händischen Überprüfung der Funktionalität nach Upgrades_

Grundsätzliches zur Umsetzung der Anpassungen: In den meisten Fällen überschreiben wir entweder Templates oder
URL-Pfade. Sollte sich beispielsweise der Name des Original-Templates in Juntagrico beim Upgrade ändern, so werden
unsere Anpassungen wirkungslos.

### Menü "Dein Menu ..." (Benutzermenü)

Das Menü-Template wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt
werden, sonst werden sie nicht sichtbar. Die genauen Anpassungen können wir bei Bedarf raussuchen (Template:
`rotebeete/templates/juntagrico/menu/user.html`).

#### Mitgliedschaft

Manche Templates für die Seite werden vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade
eingespielt werden, sonst werden sie nicht sichtbar. Die genauen Anpassungen können wir bei Bedarf raussuchen (veränderte Templates:
`rotebeete/templates/my/subscription/single.html`, `rotebeete/templates/my/subscription/snippets/part_list.html` neu: `rotebeete/templates/my/subscription/snippets/download_delivery_contract.html`).

#### Mitgliedschaft ➜ Genossenschaftsanteile verwalten

Das Template für die Seite wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade
eingespielt werden, sonst werden sie nicht sichtbar. Die genauen Anpassungen können wir bei Bedarf raussuchen (Template:
`rotebeete/templates/manage_shares.html`).

#### Mitgliedschaft ➜ Genossenschaftsanteile verwalten ➜ Bescheinigung herunterladen

Das Template für die PDF-Bescheinigung wird vollständig überschrieben. Änderungen am Juntagrico-Template werden
nicht sichtbar. Template: `rotebeete/templates/exports/share_certificate.html`

#### Mitgliedschaft ➜ Gemüseanteil ändern ➜ Bestandteile

Das Template für diese Zeile (alle Spalten) wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt
werden, sonst werden sie nicht sichtbar. Die genauen Anpassungen können wir bei Bedarf raussuchen (Template:
`rotebeete/templates/snippets/snippet_subscription_change_size.html`).

#### Persönliche Daten

Das Template für die Seite wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade
eingespielt werden, sonst werden sie nicht sichtbar.

- IBAN-Feld wird deaktiviert
- Template: `rotebeete/templates/profile.html`
- Filter: `rotebeete.templatetags.rotebeete.disable_iban`

### Menü Administration

#### Gemüseanteile ➜ Aktive

Das Menü-Templates wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt
werden, sonst werden sie nicht sichtbar. Die genauen Anpassungen können wir bei Bedarf raussuchen (Template:
`rotebeete/templates/management_lists/subscriptions.html`).

#### Listen

Das Menü-Templates wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt
werden, sonst werden sie nicht sichtbar. Die genauen Anpassungen können wir bei Bedarf raussuchen (Template:
`rotebeete/templates/juntagrico/menu/admin/lists.html`).

#### Listen ➜ Mengenübersicht

- Pfad: `/rb/export/depots`
- erzeugt eine CSV-Datei mit den Headern "Verteilstation" und "Anteile"
- Code: `rotebeete.exports.urls`

#### Listen ➜ Verteilstation-Listen

- Pfad: `/rb/export/subscriptions`
- erzeugt eine CSV-Datei mit den Headern "Verteilstation", "GLV-Nr.", ...
- Code: `rotebeete.exports.urls`

#### Listen ➜ Verteilstation eMail-Listen

- Pfad: `/rb/export/emails`
- erzeugt eine CSV-Datei mit den Headern "Verteilstation" und "E-Mail-Adresse"
- Code: `rotebeete.exports.urls`

#### Exporte

Das Template für die Seite wird vollständig überschrieben. Änderungen am Juntagrico-Template werden
nicht sichtbar. Template: `rotebeete/templates/export.html`

#### Exporte ➜ Mitglieder exportieren

- Pfad: `/rb/export/members`
- erzeugt eine CSV-Datei mit der Überschrift "Mitgliederliste Gemüsekooperative Rote Beete eG (...)"
- Code: `rotebeete.exports.urls`

#### Exporte ➜ Gemüseanteile exportieren

- Pfad: `/rb/export/subscriptions`
- erzeugt eine CSV-Datei mit den Headern "GLV-Nr.", "Geno-Nr.", ...
- Code: `rotebeete.exports.urls`

### E-Mails

#### Nach Erzeugung eines Genossenschaftsanteils

- Es wird eine Mail verschickt: "Bitte melde dich unter invalid@rotebeete.invalid ..."
- Template: `rotebeete/templates/mails/member/share_created.txt`

### Gestaltung

In `rotebeete/static/rotebeete/css/rotebeete.css` wurden einige CSS-Eigenschaften verändert. Falls sich das Original-CSS von Juntagrico ändert, müssen diese Angaben möglicherweise angepasst werden.

### Logo

In `rotebeete/static/rotebeete/css/rotebeete.css` können die entsprechenden CSS-Eigenschaften von `juntagrico_logo` sowie der Name und die Endung der gewünschten Datei geändert werden. Der Pfad `rotebeete/static/rotebeete/img/<DATEI>` sollte dennoch beibehalten werden.
