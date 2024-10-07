## Dokumentation von Anpassungen
*zur händischen Überprüfung der Funktionalität nach Upgrades*

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
* IBAN-Feld wird deaktiviert
* Template: `rotebeete/templates/profile.html`
* Filter: `rotebeete.templatetags.rotebeete.disable_iban`

### Menü Administration

#### Gemüseanteile ➜ Aktive
Das Menü-Templates wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt
werden, sonst werden sie nicht sichtbar. Die genauen Anpassungen können wir bei Bedarf raussuchen (Template:
`rotebeete/templates/management_lists/subscriptions.html`).

#### Arbeitseinsätze ➜ Übersicht
Das Menü-Templates wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt
werden, sonst werden sie nicht sichtbar. Die genauen Anpassungen können wir bei Bedarf raussuchen (Template:
`rotebeete/templates/management_lists/assignments.html`).

#### Listen
Das Menü-Templates wird vollständig überschrieben. Änderungen am Juntagrico-Template müssen beim Upgrade eingespielt
werden, sonst werden sie nicht sichtbar. Die genauen Anpassungen können wir bei Bedarf raussuchen (Template:
`rotebeete/templates/juntagrico/menu/admin/lists.html`).

#### Listen ➜ Mengenübersicht
* Pfad: `/rb/export/depots`
* erzeugt eine CSV-Datei mit den Headern "Verteilstation" und "Anteile"
* Code: `rotebeete.exports.urls`

#### Listen ➜ Verteilstation-Listen
* Pfad: `/rb/export/subscriptions`
* erzeugt eine CSV-Datei mit den Headern "Verteilstation", "GLV-Nr.", ...
* Code: `rotebeete.exports.urls`

#### Listen ➜ Verteilstation eMail-Listen
* Pfad: `/rb/export/emails`
* erzeugt eine CSV-Datei mit den Headern "Verteilstation" und "E-Mail-Adresse"
* Code: `rotebeete.exports.urls`

#### Exporte
Das Template für die Seite wird vollständig überschrieben. Änderungen am Juntagrico-Template werden
nicht sichtbar. Template: `rotebeete/templates/export.html`

#### Exporte ➜ Mitglieder exportieren
* Pfad: `/rb/export/members`
* erzeugt eine CSV-Datei mit der Überschrift "Mitgliederliste Gemüsekooperative Rote Beete eG (...)"
* Code: `rotebeete.exports.urls`

#### Exporte ➜ Gemüseanteile exportieren
* Pfad: `/rb/export/subscriptions`
* erzeugt eine CSV-Datei mit den Headern "GLV-Nr.", "Geno-Nr.", ...
* Code: `rotebeete.exports.urls`

### E-Mails

#### Nach Erzeugung eines Genossenschaftsanteils
* Es wird eine Mail verschickt: "Bitte melde dich unter invalid@rotebeete.invalid ..."
* Template: `rotebeete/templates/mails/member/share_created.txt`

### Gestaltung

In `rotebeete/static/css/rotebeete.css` wurden einige CSS-Eigenschaften verändert. Falls sich das Original-CSS von 
Juntagrico ändert, müssen diese Angaben möglicherweise angepasst werden.