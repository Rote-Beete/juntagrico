## Juntagrico und Django Versionen

`juntagrico = "1.7.10"`
`django = "^4.2.29"`

## Entwicklungsumgebung:

uv installieren (z.B mit pipx). Folgendes Befehl ausführen, um die Projektabhängigkeiten zu installieren:

```
uv sync
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
uv run python manage.py migrate
uv run python manage.py collectstatic
uv run python manage.py createsuperuser
uv run python manage.py create_member_for_superusers
uv run python manage.py runserver
```

## Email zur Überprüfung persönlicher Daten

Beispiel für Einstellungen in `.env` oder `.env.local`Datei:

```
ROTEBEETE_EMAIL_HOST=mail.<hostname>.net
ROTEBEETE_EMAIL_HOST_USER=invalid@rotebeete.invalid
ROTEBEETE_EMAIL_HOST_PASSWORD=<PW>
ROTEBEETE_EMAIL_PORT=465
ROTEBEETE_EMAIL_USE_SSL=True
ROTEBEETE_DEFAULT_FROM_EMAIL=invalid@rotebeete.invalid

```

1. Test:

```
Beispiel: uv run python manage.py sendtesttransitionmails rotebeete@rotebeete.org
```

Es kann eine Test email Addresse in `.env` oder `.env.local` Datei hinterlegt werden:

```
ROTEBEETE_TEST_EMAIL=test@test.org
```

```
Beispiel: uv run python manage.py sendtesttransitionmails
```

2. Email an alle Mitglieder verschicken:

```
uv run python manage.py sendtransitionmails
```

ACHTUNG:
Die nötigen Email-Einstellungen müssen in `.env` oder `.env.local` Datei vorgenommen werdend (s.o.). Diese werden bevor die Email verschickt werden dir zur Kontrolle angezeigt. Die verwendete Juntagrico `EmailSender` zeigt zurzeit keine Errors, falls die Emails nicht verschickt werden können. In diesem Fall werden die Mitglieder zwar stillschweigend keine Emails bekommen, sie werden aber trotzdem als in Transition markiert werden. In Admin kann man es unter `Member Transitions` wieder rückgängig machen, indem man die entsprechenden Mitglieder wieder löscht.

## Test-Dateien

s. https://juntagrico.readthedocs.io/en/latest/intro/installation.html

```
uv run python -m manage generate_testdata
uv run python -m manage generate_testdata_advanced
```

## Bieterrunden

Wir gehen zurzeit davon aus, dass jedes Mitglied nur eine einzige Mitgliedschaft hat. Falls dieses Verhalten sich ändern soll, müssen `biddings.views._UserSubscriptionMixin._get_subscription()`, `biddings.templatetags.get_bid()` und `biddings.templates.biddings.biddinground_list.html` entsprechend aktualisiert werden.

In `biddings/admin.py` wird Juntagricos `SubscriptionAdmin` Klasse durch `BiddingSubscriptionAdmin` erweitert und in Admin ersetzt. Falls `SubscriptionAdmin` in Juntagrico grundlegend geändert werden sollte, könnte es hier zu Konflikten führen.

## Dokumentation von Anpassungen

_zur händischen Überprüfung der Funktionalität nach Upgrades_

Grundsätzliches zur Umsetzung der Anpassungen: In den meisten Fällen überschreiben wir entweder Templates oder
URL-Pfade. Sollte sich beispielsweise der Name des Original-Templates in Juntagrico beim Upgrade ändern, so werden
unsere Anpassungen wirkungslos.

### Menü "Dein Menu ..." (Benutzermenü)

Das Menü-Template wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt werden, sonst werden sie nicht sichtbar.

Überschriebene Templates:
`rotebeete/templates/juntagrico/menu/user.html`

#### Mitgliedschaft

Manche Templates für die Seite werden vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade
eingespielt werden, sonst werden sie nicht sichtbar.

Überschriebene Templates:
`rotebeete/templates/juntagrico/my/subscription/single.html`
`rotebeete/templates/juntagrico/my/subscription/snippets/part_list.html`
Neues Template:
`rotebeete/templates/juntagrico/my/subscription/snippets/download_delivery_contract.html`

#### Mitgliedschaft ➜ Genossenschaftsanteile verwalten

Das Template für die Seite wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt werden, sonst werden sie nicht sichtbar.

Überschriebene Templates:
`rotebeete/templates/manage_shares.html`

#### Mitgliedschaft ➜ Genossenschaftsanteile verwalten ➜ Bescheinigung herunterladen

Das Template für die PDF-Bescheinigung wird vollständig überschrieben. Änderungen am Juntagrico-Template werden nicht sichtbar.

Überschriebene Templates:
`rotebeete/templates/exports/share_certificate.html`

#### Mitgliedschaft ➜ Gemüseanteil ändern ➜ Bestandteile

Das Template für diese Zeile (alle Spalten) wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt werden, sonst werden sie nicht sichtbar.

Überschriebene Templates:
`rotebeete/templates/snippets/snippet_subscription_change_size.html`).

#### Persönliche Daten

#### Persönliche Daten

Das Template für die Seite wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt werden, sonst werden sie nicht sichtbar.

- IBAN-Feld wird deaktiviert
- Template: `rotebeete/templates/profile.html`
- Filter: `rotebeete.templatetags.rotebeete.disable_iban`

### Menü Administration

#### Gemüseanteile ➜ Aktive

Das Menü-Templates wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt werden, sonst werden sie nicht sichtbar.

Überschriebene Templates:
`rotebeete/templates/juntagrico/manage/subscriptions/show.html`

#### Listen

Das Menü-Templates wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt werden, sonst werden sie nicht sichtbar.

Überschriebene Templates:
`rotebeete/templates/juntagrico/menu/admin/lists.html`

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
nicht sichtbar.

Veränderte Templates: `rotebeete/templates/export.html`

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

### Alle überschriebene und neue templates:

- ADMIN:
  - MENU:
    - `rotebeete/templates/juntagrico/menu/admin/lists.html`
  - Erweiterung exports:
    - `rotebeete/templates/export.html`
  - `manage/subscription`
    - `rotebeete/templates/juntagrico/manage/subscriptions/show.html`

- DEIN MENU:
  - `rotebeete/templates/juntagrico/menu/user.html`

- PERSÖNLICHE DATEN: `/my/profile`:
  - `rotebeete/templates/profile.html`

- MITGLIEDSCHAFT: `/my/subscription/<subscription_id>/`:
  - `rotebeete/templates/juntagrico/my/subscription/single.html`
  - Bestandteile:
    - `rotebeete/templates/juntagrico/my/subscription/snippets/part_list.html`

- Genossenschaftsanteile Verwalten: `my/share/manage/`:
  - `rotebeete/templates/manage_shares.html`
  - Bescheinigung: `my/share/certificate`:
    - `rotebeete/templates/exports/share_certificate.html`

- EMAIL:
  - `rotebeete/templates/mails/member/share_created.txt`

- Neu:
  - `rotebeete/templates/juntagrico/my/subscription/snippets/download_delivery_contract.html`

- Filter:
  - `rotebeete.templatetags.rotebeete.disable_iban`

- LEGACY: Gemüseanteil ändern: `my/subscription/change/overview/<int:subscription_id>/`:
  - `rotebeete/templates/snippets/snippet_subscription_change_size.html`

- LEGACY:
  - `rotebeete/templates/subscription.html`
