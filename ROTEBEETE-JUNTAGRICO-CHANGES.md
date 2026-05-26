# Template Overrides — Changelog

Changes relative to the upstream [juntagrico](https://github.com/juntagrico/juntagrico) library templates.

---

## MENU -> Administration -> Listen

### settings

```
DEPOT_LISTS = {
    "depotlist": "exports/depotlist.html",
    "depot_overview": {
        "template": "exports/depot_overview.html",
        "name": f"{VOCABULARY['depot']} eMail-Listen",
    },
    "amount_overview": "exports/amount_overview.html",
}
```
#### User-facing changes

- The submenu entry is now labelled **eMail-Listen** instead of **Übersicht**.

---

## MENU -> Administration -> Exporte

### `/my/export`

### `export.html`

#### Code diff

```diff
@@ -7,84 +7,22 @@
     </h3>
 {% endblock %}
 {% block content %}
-    {% vocabulary "member_pl" as v_member_pl %}
-    {% vocabulary "share_pl" as v_share_pl %}
-    {% vocabulary "assignment_pl" as v_assignment_pl %}
-    {% vocabulary "subscription_pl" as v_subscription_pl %}
-    <div class="alert alert-danger">
-        {% trans "Diese Exporte werden in einer zukünftigen Version entfernt. Sprich mit deiner/m System-Admin, falls die neuen Exporte deine Anforderungen nicht abdecken." %}
-    </div>
     <div class="row mb-4">
-        <div class="col-md-3">
-            {{ v_member_pl }}
-        </div>
-        <div class="col-md-3">
-            <a href="{% url 'export-members' %}">
-                {% trans "exportieren" %}
-            </a>
-        </div>
-        <div class="col-md-6">
-            <div class="alert alert-warning">
-                {% trans "Neu: Datenverwaltung" %}
-                <a href="{% url 'admin:juntagrico_member_changelist' %}">&rarr; {{ v_member_pl }}</a>
-                {% trans "&rarr; Exportieren (oben rechts)" %}
-                {% trans "&rarr; Ressource:" %} "{{ v_member_pl }}"
-            </div>
+        <div class="col-md-3">Mitglieder</div>
+        <div class="col-md-9">
+            <a href="{% url 'export-members' %}">exportieren</a>
         </div>
     </div>
     <div class="row mb-4">
-        <div class="col-md-3">
-            {% blocktrans %}{{ v_member_pl }} mit {{ v_assignment_pl }} und Tätigketsbereichen{% endblocktrans %}
-        </div>
-        <div class="col-md-3">
-            <a href="{% url 'export-membersfilter' %}">
-                {% trans "exportieren" %}
-            </a>
-        </div>
-        <div class="col-md-6">
-            <div class="alert alert-warning">
-                {% trans "Neu: Datenverwaltung" %}
-                <a href="{% url 'admin:juntagrico_member_changelist' %}">&rarr; {{ v_member_pl }}</a>
-                {% trans "&rarr; Exportieren (oben rechts)" %}
-                {% trans "&rarr; Ressource:" %} "{{ v_member_pl }} {% trans "mit ..." %}"
-            </div>
+        <div class="col-md-3">Gemüseanteile</div>
+        <div class="col-md-9">
+            <a href="{% url 'export-subscriptions' %}">exportieren</a>
         </div>
     </div>
-    {% config "enable_shares" as c_enable_shares %}
-    {% if c_enable_shares %}
-        <div class="row mb-4">
-            <div class="col-md-3">
-                {{ v_share_pl }}
-            </div>
-            <div class="col-md-3">
-                <a href="{% url 'export-shares' %}">
-                    {% trans "exportieren" %}
-                </a>
-            </div>
-            <div class="col-md-6">
-                <div class="alert alert-warning">
-                    {% trans "Neu: Datenverwaltung" %}
-                    <a href="{% url 'admin:juntagrico_share_changelist' %}">&rarr; {{ v_share_pl }}</a>
-                    {% trans "&rarr; Exportieren (oben rechts)" %}
-                </div>
-            </div>
-        </div>
-    {% endif %}
     <div class="row mb-4">
-        <div class="col-md-3">
-            {{ v_subscription_pl }}
-        </div>
-        <div class="col-md-3">
-            <a href="{% url 'export-subscriptions' %}">
-                {% trans "exportieren" %}
-            </a>
-        </div>
-        <div class="col-md-6">
-            <div class="alert alert-warning">
-                {% trans "Neu: Datenverwaltung" %}
-                <a href="{% url 'admin:juntagrico_subscription_changelist' %}">&rarr; {{ v_subscription_pl }}</a>
-                {% trans "&rarr; Exportieren (oben rechts)" %}
-            </div>
+        <div class="col-md-3">Bietrunden</div>
+        <div class="col-md-9">
+            <a href="{% url 'export-bidding-rounds' %}">Export-Übersicht</a>
         </div>
     </div>
 {% endblock %}
```

#### User-facing changes

- The deprecation warning is removed entirely.
- Only three export rows remain: **Mitglieder**, **Gemüseanteile**, **Bietrunden**.
- Rows for _Mitglieder mit Tätigkeitsbereichen_ and conditional _Genossenschaftsanteile_ are removed.
- **Bietrunden** row added with a link to `export-bidding-rounds`.

## MENU -> Administration -> Gemüseanteile -> Aktive

### `/manage/subscription`

### `juntagrico/manage/subscription/show.html`

#### Code diff

```diff
@@ -1,96 +1,57 @@
-{% extends "../base.html" %}
+{% extends "management_lists/man_list_base.html" %}
 {% load i18n %}
 {% load static %}
 {% load juntagrico.config %}
 {% load juntagrico.common %}
 {% load juntagrico.snippets %}
-
 {% block page_title %}
     <h3>
         {{ title }}
     </h3>
 {% endblock %}
-
-{% block content %}
-    {% include '../member/snippets/toggle_buttons.html' with co_members=True %}
-    {{ block.super }}
+{% block management_cmd %}
+    {% include 'management_lists/snippets/email_sender.html' %}
 {% endblock %}
-
 {% block list %}
     <table id="filter-table" class="list table">
         <thead>
             <tr>
-                {% block list_head %}
-                    <th class="filter">
-                        {% vocabulary "subscription" %}
-                    </th>
-                    <th class="filter">
-                        {% trans "Inhalt" %}
-                    </th>
-                    {% if not hide_depots %}
-                        <th class="filter">
-                            {% vocabulary "depot" %}
-                        </th>
-                    {% endif %}
-                    <th class="filter">
-                        {% trans "Aktivierungsdatum" %}
-                    </th>
-                    <th class="filter">
-                        {% trans "Kontakt" %}
-                    </th>
-                {% endblock %}
+                <th class="filter">{% trans "HauptbezieherIn" %}</th>
+                <th class="filter">{% trans "Weitere BezieherInnen" %}</th>
+                <th class="filter">{% vocabulary "depot" %}</th>
+                <th class="filter">{% trans "Inhalt" %}</th>
+                <th class="filter">{% trans "Aktivierungsdatum" %}</th>
+                <th class="filter">{% trans "E-Mails" %}</th>
             </tr>
         </thead>
         <tfoot>
             <tr>
-                {% block list_foot %}
-                    <th>
-                        {% vocabulary "subscription" %}
-                    </th>
-                    <th>
-                        {% trans "Inhalt" %}
-                    </th>
-                    {% if not hide_depots %}
-                        <th>
-                            {% vocabulary "depot" %}
-                        </th>
-                    {% endif %}
-                    <th>
-                        {% trans "Aktivierungsdatum" %}
-                    </th>
-                    <th>
-                        {% trans "Kontakt" %}
-                    </th>
-                {% endblock %}
+                <th>{% trans "HauptbezieherIn" %}</th>
+                <th>{% trans "Weitere BezieherInnen" %}</th>
+                <th>{% vocabulary "depot" %}</th>
+                <th>{% trans "Inhalt" %}</th>
+                <th>{% trans "Aktivierungsdatum" %}</th>
+                <th>{% trans "E-Mails" %}</th>
             </tr>
         </tfoot>
         <tbody>
-            {% for subscription in object_list %}
-                {% block list_entry %}
-                    <tr>
-                        <td>
-                            {% include './snippets/display_linked.html' %}
-                        </td>
-                        <td>
-                            {% for item in subscription.content_strings %}
-                                <div>
-                                    {{ item }}
-                                </div>
-                            {% endfor %}
-                        </td>
-                        {% if not hide_depots %}
-                            <td>
-                                {{ subscription.depot.name }}
-                            </td>
+            {% for subscription in subscriptions %}
+                <p>subscription</p>
+                <tr>
+                    <td>
+                        {% if subscription.primary_member %}
+                            {% impersonate_start request subscription.primary_member %}
+                            <a href="{% url 'admin:juntagrico_member_change' subscription.primary_member.id %}">
+                                {{ subscription.primary_member.get_name }}
+                            </a>
                         {% endif %}
-                        <td>
-                            {{ subscription.activation_date|date:"Y-m-d" }}
-                        </td>
-                        <td>
-                            {% include './snippets/members_linked.html' %}
-                        </td>
-                    </tr>
-                {% endblock %}
+                    </td>
+                    <td>{{ subscription.comembers }}</td>
+                    <td>{{ subscription.depot.name }}</td>
+                    <td>{{ subscription }}</td>
+                    <td>{{ subscription.activation_date|date:"Y-m-d" }}</td>
+                    <td class="email">{{ subscription.recipients_qs|values_list:'member__email'|join:', ' }}</td>
+                </tr>
             {% endfor %}
         </tbody>
     </table>
```

#### User-facing changes

- The table now shows **HauptbezieherIn** (linked to admin), **Weitere BezieherInnen**, **Depot**, **Inhalt**, **Aktivierungsdatum**, **E-Mails** — replacing the previous generic columns.
- An **email sender** snippet is added above the table.
- The toggle buttons for co-members view are removed.

---

## DEIN MENU

### `juntagrico/menu/user.html`

#### Code diff

```diff
@@ -13,12 +13,12 @@
     </li>
     <li class="nav-item">
         <a class="nav-link {{ request|activemenu:"subscription" }}" href="{% url 'subscription-landing' %}">
-            {{ v_subscription }}
+            Mitgliedschaft
         </a>
     </li>
     <li class="nav-item">
         <a class="nav-link {{ request|activemenu:"jobs" }}" href="{% url 'jobs' %}">
-            {% trans "Einsätze" %}
+            {% trans "Mitarbeitskalender" %}
         </a>
         {% if request|activemenu:"jobs" == 'active' %}
             <ul class="nav flex-column sub-menu">
@@ -35,21 +35,24 @@
             </ul>
         {% endif %}
     </li>
-    {% if b_show_deliveries %}
-        <li class="nav-item">
-            <a class="nav-link {{ request|activemenu:"deliveries" }}" href="{% url 'deliveries' %}">
-                {% trans "Lieferungen" %}
-            </a>
-        </li>
-    {% endif %}
+    <li class="nav-item">
+        <a class="nav-link {{ request|activemenu:"deliveries" }}" href="{% url 'deliveries' %}">
+            {% trans "Lieferungen" %}
+        </a>
+    </li>
     <li class="nav-item">
         <a class="nav-link {{ request|activemenu:"area" }}" href="{% url 'areas' %}">
             {% trans "Tätigkeitsbereiche" %}
         </a>
     </li>
     <li class="nav-item">
+        <a class="nav-link {{ request|activemenu:"area" }}" href="{% url 'biddingrounds' %}">
+            {% trans "Bietrunden" %}
+        </a>
+    </li>
+    <li class="nav-item">
         <a class="nav-link {{ request|activemenu:"membership" }}" href="{% url 'profile' %}">
-            {% trans "Mitgliedschaft" %}
+            {% trans "Persönliche Daten" %}
         </a>
     </li>
     <li class="nav-item">
@@ -64,10 +67,8 @@
     {% endblock %}
     <li class="separator">
     </li>
-    <li class="nav-item main-menu-small">
-        <a class="nav-link yellow" href="{% organisation_website "url" %}">
-            {% organisation_website "name" %}
-        </a>
+    <li class="nav-item">
+        <a class="nav-link" href="https://wiki.rotebeete.org/">Wiki</a>
     </li>
     <li class=" nav-item main-menu-small">
         <a class="nav-link yellow" href="{% url 'logout' %}">
```

#### User-facing changes

- "Gemüseanteil" renamed to "Mitgliedschaft"
- "Einsätze" renamed to "Mitarbeitskalender"
- "Lieferungen" now always displayed (was conditional)
- **Bietrunden** menu item added
- "Mitgliedschaft" menu label changed to "Persönliche Daten"
- Organization website link replaced with wiki.rotebeete.org link

---

## PERSÖNLICHE DATEN

### `/my/profile`

### `profile.html`

#### Code diff

```diff
@@ -5,84 +5,57 @@

 {% block page_title %}
     <h3>
-        {% trans "Mitgliedschaft" %}
+        {% trans "Persönliche Daten" %}
     </h3>
 {% endblock %}

 {% block content %}
-    {% block membership %}
-        <div class="row mb-5 membership-status">
-            <div class="col-md-3">
-                {% trans "Status" %}
-            </div>
-            <div class="col-md-9">
-                {% if member.canceled %}
-                    <div class="alert alert-warning">
-                        {% block info_canceled %}
-                            {% blocktrans trimmed with cd=member.cancellation_date|date:"d.m.Y" v_member_type=vocabulary.member_type %}
-                                Deine {{ v_member_type }}schaft ist seit dem {{ cd }} gekündigt.
-                            {% endblocktrans %}
-                        {% endblock %}
-                    </div>
-                {% elif not member.inactive%}
-                    <div class="alert alert-success">
-                        {% block info_active %}
-                            {% blocktrans with v_member_type=vocabulary.member_type %}Deine {{ v_member_type }}schaft ist aktiv.{% endblocktrans %}
-                        {% endblock %}
-                    </div>
-                {% endif %}
+    {% vocabulary "member_type" as v_member_type %}

-                {% if member.number %}
-                    <p>
-                        {% blocktrans trimmed with number=member.number %}
-                            Nummer: {{ number }}
-                        {% endblocktrans %}
-                    </p>
-                {% endif %}
+    {% if success %}
+        <div class="alert alert-success">
+            {% trans "Personalien erfolgreich geändert" %}
+        </div>
+    {% endif %}

-                {% if not member.canceled %}
-                    {% block button_cancel_membership %}
-                        <a href="{% url 'cancel-membership' %}" class="btn btn-outline-danger">
-                            {% trans "Mitgliedschaft künden" %}
-                        </a>
-                    {% endblock %}
-                {% endif %}
+    {% include "transitions/_review_data_confirm.html" %}
+
+    {% if member.canceled %}
+        <div class="alert alert-warning">
+            {% blocktrans trimmed with cd=member.cancellation_date|date:"d.m.Y" %}
+                Deine {{ v_member_type }}schaft ist seit dem {{ cd }} gekündigt.
+            {% endblocktrans %}
+        </div>
+    {% endif %}
+
+    {% if not member.canceled and not member.inactive %}
+        <div class="alert alert-success">
+            {% blocktrans %}Deine {{ v_member_type }}schaft ist aktiv.{% endblocktrans %}
+        </div>
+    {% endif %}
+
+    <form method="post" class="mb-4">
+        {% load rotebeete %}
+        {% with form=memberform|disable_iban %}
+            {% crispy form %}
+        {% endwith %}
+    </form>
+
+    <div class="row mb-2">
+        <div class="offset-md-3 col-md-9">
+            <a href="{% url 'password' %}" class="btn btn-success">
+                {% trans "Passwort ändern" %}
+            </a>
+        </div>
+    </div>
+
+    {% if not member.canceled %}
+        <div class="row mb-2">
+            <div class="offset-md-3 col-md-9">
+                <a href="{% url 'cancel-membership' %}" class="btn btn-danger">
+                    {% trans "Mitgliedschaft künden" %}
+                </a>
             </div>
         </div>
-    {% endblock %}
-
-    {% block documents %}
-        {% include "juntagrico/snippets/documents.html" %}
-    {% endblock %}
-
-    {% block password %}
-        <div class="row mb-5 password">
-            <div class="col-md-3">
-                {% trans "Passwort" %}
-            </div>
-            <div class="col-md-9">
-                {% block button_change_password %}
-                    <a href="{% url 'password' %}" class="btn btn-primary">
-                        {% trans "Passwort ändern" %}
-                    </a>
-                {% endblock %}
-            </div>
-        </div>
-    {% endblock %}
-
-    {% block profile %}
-        <div class="mb-5">
-            <h4>
-                {% trans "Personalien" %}
-            </h4>
-            {% if success %}
-                <div class="alert alert-success">
-                    {% trans "Personalien erfolgreich geändert" %}
-                </div>
-            {% endif %}
-            <form method="post" class="mb-4">
-                {% crispy memberform %}
-            </form>
-        </div>
-    {% endblock %}
+    {% endif %}
 {% endblock %}
```

#### User-facing changes

- Page title changed from **Mitgliedschaft** to **Persönliche Daten**
- Data review/confirmation widget added at the top
- **IBAN field is disabled** (read-only) in the member form
- Documents section removed
- Password and cancellation buttons are always visible (simplified layout, no nested blocks)

---

## MITGLIEDSCHAFT

### `my/subscription/<subscription-id>/`

### `juntagrico/my/subscription/single.html`

#### Code diff

```diff
@@ -55,12 +55,9 @@
         {% include 'juntagrico/my/assignment/snippets/subscription_overview.html' %}
         {# Share #}
         {% include 'juntagrico/my/share/snippets/subscription_overview.html' %}
-        {# Documents #}
-        {% block documents %}
-            {% include "juntagrico/snippets/documents.html" %}
-        {% endblock %}
         {# Additional #}
-        {% block extend %}
-        {% endblock %}
+        {% include 'juntagrico/my/subscription/snippets/download_delivery_contract.html' %}
+        {% include "transitions/_review_membership_confirm.html" %}
+        {% block extend %}{% endblock %}
     {% endwith %}
 {% endblock %}
```

#### User-facing changes

- **Documents section replaced** with GLV (delivery contract) download link
- **Membership review confirmation (transitions) widget** added

---

## MITGLIEDSCHAFT

### `juntagrico/my/subscription/snippets/part_list.html`

### `my/subscription/<subscription-id>/`

#### Code diff

```diff
 {% load crispy_forms_tags %}
 {% load i18n %}
 {% load juntagrico.subscription %}
 {% if parts.exists %}
     <table class="table subscription-table">
         <thead>
             <tr>
-                <th>{% trans "Name" %}</th>
+                <th>{% trans "GVL-Nr." %}</th>
+                <th>{% trans "Anzahl Anteile" %}</th>
+                <th>{% trans "Monatl. Beitrag" %}</th>
                 <th>{% trans "Status" %}</th>
                 <th></th>
             </tr>
         </thead>
         <tbody>
-                <td>{{ part }}</td>
-                <td>{{ part.state_text }}</td>
-                <td>
-                    {% if part.cancellation_date %}
-                        {% blocktrans trimmed with cd=part.cancellation_date %}
+                    <td>{{ part.type.name }}</td>
+                    <td>{{ part.type.size.units }}</td>
+                    <td>{{ part.type.price }}</td>
+                    <td>{{ part.state_text }}</td>
+                    <td>
+                        {% if part.cancellation_date %}
+                            {% blocktrans with cd=part.cancellation_date %}
                             Gekündigt am {{ cd }}
                         {% endblocktrans %}
-                            {% blocktrans trimmed with dd=part.deactivation_date %}
+                                {% blocktrans with dd=part.deactivation_date %}
                                 Noch aktiv bis am {{ dd }}
                             {% endblocktrans %}
-                        {% endif %}
-                    {% else %}
-                        {% with ad=part.activation_date %}
-                            {% if part.active %}
-                                {% blocktrans %}Aktiv seit {{ ad }}{% endblocktrans %}
-                                <br>
-                            {% elif ad %}
-                                {% blocktrans %}Wird aktiv am {{ ad }}{% endblocktrans %}
-                                <br>
                             {% endif %}
-                        {% endwith %}
-                        {% if subscription.primary_member == member %}
-                            {% if part.is_extra %}
-                                {% if part.state != 'canceled' and  part.state != 'inactive' %}
-                                    <a href="{% url 'part-cancel' part.id subscription.id %}" class="btn btn-danger"
-                                    onclick="return confirm('{% trans "Bist du sicher, dass du dieses Zusatzabo kündigen möchtest?" %}')">
-                                        {% trans "kündigen" %}
-                                    </a>
+                        {% else %}
+                            {% with ad=part.activation_date %}
+                                {% if part.active %}
+                                    {% blocktrans %}
+                                    Aktiv seit {{ ad }}
+                                {% endblocktrans %}
+                                    <br>
+                                {% elif ad %}
+                                    {% blocktrans %}
+                                    Wird aktiv am {{ ad }}
+                                {% endblocktrans %}
+                                    <br>
                                 {% endif %}
-                            {% else %}
-                                {% if can_change_part %}
+                            {% endwith %}
+                            {% if subscription.primary_member == member %}
+                                {% if part.is_extra %}
+                                    {% if part.state != 'canceled' and  part.state != 'inactive' %}
+                                        <a href="{% url 'part-cancel' part.id subscription.id %}"
+                                           class="btn btn-danger"
+                                           onclick="return confirm('{% trans "Bist du sicher, dass du dieses Zusatzabo kündigen möchtest?" %}')">
+                                            {% trans "kündigen" %}
+                                        </a>
+                                    {% endif %}
+                                {% else %}
+                                    {% comment %} {% if can_change_part %}
                                     <a href="{% url 'part-change' part.id %}" class="btn btn-primary">
                                         {% trans "ändern" %}
                                     </a>
-                                {% endif %}
-                                {% if part.subscription.future_parts.is_normal.count == 1 %}
-                                    {% if part.subscription.state != 'canceled' and  part.subscription.state != 'inactive' %}
-                                        <a href="{% url 'sub-cancel' subscription.id %}" class="btn btn-danger">
-                                            {% blocktrans %}{{ v_subscription }} komplett künden{% endblocktrans %}
+                                    {% endif %} {% endcomment %}
+                                    {% if part.subscription.future_parts.is_normal.count == 1 %}
+                                        {% if part.subscription.state != 'canceled' and  part.subscription.state != 'inactive' %}
+                                            <a href="{% url 'sub-cancel' subscription.id %}" class="btn btn-danger">
+                                                {% blocktrans %}{{ v_subscription }} komplett künden{% endblocktrans %}
+                                            </a>
+                                        {% endif %}
+                                    {% elif part.subscription.future_parts.is_normal.count > 1 %}
+                                        <a href="{% url 'part-cancel' part.id subscription.id %}"
+                                           class="btn btn-danger"
+                                           onclick="return confirm('{% trans "Bist du sicher, dass du diesen Bestandteil kündigen möchtest?" %}')">
+                                            {% trans "kündigen" %}
+                                        </a>
+                                    {% endif %}
                                 {% endif %}
-                                {% elif part.subscription.future_parts.is_normal.count > 1 %}
-                                    <a href="{% url 'part-cancel' part.id subscription.id %}" class="btn btn-danger"
-                                    onclick="return confirm('{% trans "Bist du sicher, dass du diesen Bestandteil kündigen möchtest?" %}')">
-                                        {% trans "kündigen" %}
-                                    </a>
                             {% endif %}
                         {% endif %}
                     </td>
```

#### User-facing changes

- Table columns changed from **Name** to **GVL-Nr.**, **Anzahl Anteile**, **Monatl. Beitrag**, plus **Status**
- Part display now shows `part.type.name`, `part.type.size.units`, and `part.type.price` instead of just `{{ part }}`
- The "ändern" (edit) button is commented out and hidden

---

## MITGLIEDSCHAFT: Genossenschaftsanteile Verwalten

### `/my/share/manage/`

### `manage_shares.html`

#### Code diff

```diff
@@ -70,20 +70,15 @@
                                 <td>
                                     {% if forloop.first %}
                                         {% blocktrans %}Du brauchst mindestens 1 {{ v_share }}{% endblocktrans %}
-                                        {% if not required %}
-                                            <div>
-                                                <a href="{% url 'cancel-membership' %}" class="btn btn-outline-danger">
-                                                    {% trans "Mitgliedschaft kündigen" %}
-                                                </a>
-                                            </div>
-                                        {% endif %}
                                     {% elif forloop.counter <= required %}
                                         {% blocktrans %}Diese/s/r {{ v_share }} wird in einem/r {{ v_subscription }} benötigt{% endblocktrans %}
+                                    {% elif share.cancelled_date is None and share.paid_date is None %}
+                                        {% blocktrans %}Diese/s/r {{ v_share }} wurde noch nicht als bezahlt verbucht{% endblocktrans %}
                                     {% elif ibanempty %}
                                         <a href="{% url 'profile' %}">{% blocktrans %}Kann gekündigt werden, sobald eine IBAN hinterlegt ist{% endblocktrans %}</a>
-                                    {% elif share.cancelled_date is None %}
-                                        <a href="{% url 'share-cancel' share.id %}" class="btn btn-outline-danger"
-                                           onclick="return confirm('{% blocktrans %} Möchtest du diese/s/n {{ v_share }} verbindlich zum {{ next_membership_end_date }} kündigen? {% endblocktrans%}')">
+                                    {% elif share.cancelled_date is None and share.paid_date is not None %}
+                                        <a href="{% url 'share-cancel' share.id %}" class="btn btn-success"
+                                           onclick="return confirm('{% blocktrans %} Möchtest du sicher diese/s/n {{ v_share }} verbindlich kündigen? {% endblocktrans%}')">
                                             {% trans "kündigen" %}
                                         </a>
                                     {% endif %}
@@ -95,25 +90,6 @@
             </div>
         {% endif %}
     {% endblock %}
-
-    {% block order %}
-        <h5>{% blocktrans %}{{ v_share_pl }} bestellen{% endblocktrans %}</h5>
-        {% if shareerror %}
-            <div class="alert alert-danger">
-                {% trans "Deine Eingabe ist ungültig" %}
-            </div>
-        {% endif %}
-        <form method="post" class="form-inline">
-            {% csrf_token %}
-            <div class="form-group">
-                <label for="shares_input" class="mr-2">{{ v_share_pl }}</label>
-                <input type="number" name="shares" id="shares_input" class="form-control" value="0" min="0"/>
-                <button type="submit" class="ml-2 btn btn-success">
-                    {% blocktrans %}Bestellen{% endblocktrans %}
-                </button>
-            </div>
-        </form>
-    {% endblock %}
 {% endblock %}

 {% block scripts %}
```

#### User-facing changes

- **Share ordering form removed completely** — users can no longer order new shares from this page
- **Conditional cancellation logic added**:
  - If share is unpaid (`paid_date is None`): shows "noch nicht als bezahlt verbucht"
  - If no IBAN on file (`ibanempty`): shows message to add IBAN first
  - If share is paid and not cancelled: shows cancellation button with confirmation dialog

---

## MITGLIEDSCHAFT: Genossenschaftsanteile Verwalten: Bescheinigung herunterladen

### `exports/share_certificate.html`

#### Code diff

```diff
@@ -97,7 +97,7 @@

 <p class="member">
     Name: {{ member.first_name }} {{ member.last_name }}<br>
-    {{ v_member }}-Nr.: {{ member.id }}
+    {{ v_member }}-Nr.: {{ member.share_set.first.number }}
 </p>
 <p class="main_text">
     {% blocktrans trimmed %}
```

#### User-facing changes

- **Member number on certificate now displays the share number** (`member.share_set.first.number`) instead of internal member ID

---

## E-MAILS

### `mails/member/share_created.txt`

#### Code diff

```diff
@@ -1,35 +1,4 @@
 {% extends "mails/email.txt" %}
-{% load i18n %}
-{% load juntagrico.config %}
 {% block content %}
-{% config "organisation_address" as c_addr %}
-{% config "organisation_bank_connection" as c_bank %}
-{% config "share_price" as c_share_price %}
-{% config "currency" as c_currency %}
-{% config "organisation_name" as c_organisation_name %}
-{% enriched_organisation "D" as v_d_enriched_organisation %}
-{% vocabulary "share" as v_share %}
-{% vocabulary "share_pl" as v_share_pl %}
-{% trans "Hallo" %}
-
-{% blocktrans with sc=shares|length%}Du hast bei {{ v_d_enriched_organisation }} {{sc}} {{ v_share_pl }} bestellt{% endblocktrans %}:
-{% for share in shares %}{% blocktrans with sid=share.id %}{{ v_share }} mit Systemnummer {{ sid }}{% endblocktrans %}
-{% endfor %}
-{% blocktrans with sc=shares|length %}Bitte überweise {{sc}} Mal den Betrag von {{ c_currency }} {{ c_share_price }} auf das folgende Konto{% endblocktrans %}:
-    {{ c_addr.name }}
-    {% if c_addr.extra %}{{ c_addr.extra }}{% endif %}
-    {{ c_addr.street }} {{ c_addr.number }}
-    {{ c_addr.zip }} {{ c_addr.city }}
-    {{ c_bank.NAME }}
-    {% trans "Postkonto-Nummer" %}: {{ c_bank.PC }}
-    {% trans "IBAN" %}: {{ c_bank.IBAN }}
-    {% trans "BIC" %}: {{ c_bank.BIC }}
-
-{% blocktrans %}Um die Arbeit der Buchhaltung zu erleichtern zahle bitte nur 1 {{ v_share }} auf einmal.
-Gib im Betreff die Systemnummer an und die Emailadresse der Halterin oder des Halters des/r {{ v_share }} an
-(dies ist vor allem wichtig wenn du diese/n/s {{ v_share }} für jemand anderen bezahlst){% endblocktrans %}
-
-{% blocktrans trimmed %}
-Bis bald und liebe Grüsse die {{ c_organisation_name }}-Betriebsgruppe
-{% endblocktrans %}
+Bitte melde dich unter invalid@rotebeete.invalid für das weitere Vorgehen. Danke.
 {% endblock %}
```

#### User-facing changes

- **Completely simplified email** - removed payment instructions and bank details
- Members now directed to **invalid@rotebeete.invalid** to handle payment outside of system
- No more inline payment information in email

---

## NEU (kein Original in Juntagrico)

### `juntagrico/my/subscription/snippets/download_delivery_contract.html`

New template — no upstream counterpart.

#### Content

```html
{% load i18n %}
{% if subscription.state == 'active' and subscription.primary_member == member %}
    <div class="row mb-3">
        <div class="col-md-3">{% trans "GLV-Download" %}</div>
        <div class="col-md-9">
            <a href="{% url "download-delivery-contract" %}">{% trans "Aktuellen Gemüseliefervertrag herunterladen" %}</a>
        </div>
    </div>
{% endif %}
```

#### User-facing changes

- New template provides **GLV (delivery contract) download** link for active primary members on their subscription detail page
- Only visible for **active subscriptions** where the user is the **primary member**
