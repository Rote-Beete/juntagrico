# Template Overrides — Changelog

Changes relative to the upstream [juntagrico](https://github.com/juntagrico/juntagrico) library templates.

---

## ADMIN

### `juntagrico/menu/admin/lists.html`

#### Code diff

```diff
@@ -7,35 +7,25 @@
             <i class="fas fa-angle-right">
             </i>
         </a>
-        <div class="collapse {% if 'manage-list' in request.resolver_match.url_name %} show{% endif %}" id="lists">
+        <div class="collapse" id="lists">
             <ul class="nav flex-column admin-menu subadmin-menu">
-                {% block sub %}
-                    {% if perms.juntagrico.can_generate_lists %}
-                        <li class="nav-item">
-                            <a class="nav-link" href="{% url 'manage-list' %}">
-                                {% trans "Erzeugen" %}
-                            </a>
-                        </li>
-                    {% endif %}
-                    {% if perms.juntagrico.can_view_lists %}
-                        <li class="nav-item">
-                            <a class="nav-link" href="{% url 'lists-depot-amountoverview' %}">
-                                {% trans "Mengen Übersicht" %}
-                            </a>
-                        </li>
-                        <li class="nav-item">
-                            <a class="nav-link" href="{% url 'lists-depotlist' %}">
-                                {% vocabulary "depot" %}-{% trans "Listen" %}
-                            </a>
-                        </li>
-                        <li class="nav-item">
-                            <a class="nav-link" href="{% url 'lists-depot-overview' %}">
-                                {% vocabulary "depot" %} {% trans "Übersicht" %}
-                            </a>
-                        </li>
-                    {% endif %}
-                {% endblock %}
+                {% if perms.juntagrico.can_generate_lists %}
+                    <li class="nav-item">
+                        <a class="nav-link" href="{% url 'manage-list' %}">{% trans "Erzeugen" %}</a>
+                    </li>
+                {% endif %}
+                {% if perms.juntagrico.can_view_lists %}
+                    <li class="nav-item">
+                        <a class="nav-link" href="{% url 'lists-depot-amountoverview' %}">{% trans "Mengen Übersicht" %}</a>
+                    </li>
+                    <li class="nav-item">
+                        <a class="nav-link" href="{% url 'lists-depotlist' %}">{% vocabulary "depot" %}-{% trans "Listen" %}</a>
+                    </li>
+                    <li class="nav-item">
+                        <a class="nav-link" href="{% url 'lists-depot-overview' %}">{% vocabulary "depot" %} {% trans "eMail-Listen" %}</a>
+                    </li>
+                {% endif %}
             </ul>
         </div>
     </li>
-{% endif %}+{% endif %}

```

#### User-facing changes

- The _Listen_ submenu no longer auto-expands when navigating to the list-generation page.
- The last submenu entry is now labelled **eMail-Listen** instead of **Übersicht**.

---

### `export.html`

#### Code diff

```diff
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

### `juntagrico/manage/subscription/show.html`

#### Code diff

```diff
-{% extends "../base.html" %}
+{% extends "management_lists/man_list_base.html" %}
 {% load i18n %}
 {% load static %}
 {% load juntagrico.config %}
 {% load juntagrico.common %}
 {% load juntagrico.snippets %}
-{% block page_title %}
-    <h3>
-        {{ title }}
-    </h3>
+{% block page_title %}<h3>{{ title }}</h3>{% endblock %}
+{% block management_cmd %}
+    {% include 'management_lists/snippets/email_sender.html' %}
 {% endblock %}
-{% block content %}
-    {% include '../member/snippets/toggle_buttons.html' with co_members=True %}
-    {{ block.super }}
-{% endblock %}
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
-                        {% endif %}
-                        <td>
-                            {{ subscription.activation_date|date:"Y-m-d" }}
-                        </td>
-                        <td>
-                            {% include './snippets/members_linked.html' %}
-                        </td>
-                    </tr>
-                {% endblock %}
+            {% for subscription in subscriptions %}
+                <tr>
+                    <td>
+                        {% if subscription.primary_member %}
+                            <a href="{% url 'admin:juntagrico_member_change' subscription.primary_member.id %}">
+                                {{ subscription.primary_member.get_name }}
+                            </a>
+                        {% endif %}
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
 {% vocabulary "subscription" as v_subscription %}
 <ul class="main-menu nav flex-column">
     <li>
     </li>
     <li class="nav-item">
-        <a class="nav-link {{ request|activemenu:"subscription" }}" href="{% url 'subscription-landing' %}">
-            {{ v_subscription }}
-        </a>
+        <a class="nav-link {{ request|activemenu:"subscription" }}"
+           href="{% url 'subscription-landing' %}">Mitgliedschaft</a>
     </li>
     <li class="nav-item">
-        <a class="nav-link {{ request|activemenu:"jobs" }}" href="{% url 'jobs' %}">
-            {% trans "Einsätze" %}
-        </a>
+        <a class="nav-link {{ request|activemenu:"jobs" }}"
+           href="{% url 'jobs' %}">{% trans "Mitarbeitskalender" %}</a>
         {% if request|activemenu:"jobs" == 'active' %}
             <ul class="nav flex-column sub-menu">
                 <li class="nav-item">
                 </li>
                 <li class="nav-item">
                 </li>
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
+    {# {% if b_show_deliveries %} #}
     <li class="nav-item">
-        <a class="nav-link {{ request|activemenu:"area" }}" href="{% url 'areas' %}">
-            {% trans "Tätigkeitsbereiche" %}
-        </a>
+        <a class="nav-link {{ request|activemenu:"deliveries" }}"
+           href="{% url 'deliveries' %}">{% trans "Lieferungen" %}</a>
+    </li>
+    {# {% endif %} #}
+    <li class="nav-item">
+        <a class="nav-link {{ request|activemenu:"area" }}"
+           href="{% url 'areas' %}">{% trans "Tätigkeitsbereiche" %}</a>
     </li>
     <li class="nav-item">
-        <a class="nav-link {{ request|activemenu:"membership" }}" href="{% url 'profile' %}">
-            {% trans "Mitgliedschaft" %}
-        </a>
+        <a class="nav-link {{ request|activemenu:"area" }}"
+           href="{% url 'biddingrounds' %}">{% trans "Bietrunden" %}</a>
     </li>
     <li class="nav-item">
-        <a class="nav-link {{ request|activemenu:"contact" }}" href="{% url 'contact' %}">
-            {% trans "Kontakt" %}
-        </a>
+        <a class="nav-link {{ request|activemenu:"membership" }}"
+           href="{% url 'profile' %}">{% trans "Persönliche Daten" %}</a>
+    </li>
+    <li class="nav-item">
+        <a class="nav-link {{ request|activemenu:"contact" }}"
+           href="{% url 'contact' %}">{% trans "Kontakt" %}</a>
     </li>
     {% for user_menu in l_user_menus %}
         {% include user_menu %}
     {% endfor %}
-    {% block extend %}
-    {% endblock %}
-    <li class="separator">
-    </li>
-    <li class="nav-item main-menu-small">
-        <a class="nav-link yellow" href="{% organisation_website "url" %}">
-            {% organisation_website "name" %}
-        </a>
+    <li class="separator"></li>
+    <li class="nav-item">
+        <a class="nav-link" href="https://wiki.rotebeete.org/">Wiki</a>
     </li>
     <li class=" nav-item main-menu-small">
     </li>
 </ul>
```

#### User-facing changes

- Menu header simplified to single line
- "Einsätze" renamed to "Mitarbeitskalender"
- "Lieferungen" now always displayed (was conditional)
- **Bietrunden** menu item added
- "Mitgliedschaft" menu label changed to "Persönliche Daten"
- Organization website link replaced with wiki.rotebeete.org link

---

## PERSÖNLICHE DATEN

### `profile.html`

#### Code diff

```diff
 {% load i18n %}
 {% load juntagrico.config %}
 {% load crispy_forms_tags %}
 {% block page_title %}
-    <h3>
-        {% trans "Mitgliedschaft" %}
-    </h3>
+    <h3>{% trans "Persönliche Daten" %}</h3>
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
-                {% if member.number %}
-                    <p>
-                        {% blocktrans trimmed with number=member.number %}
-                            Nummer: {{ number }}
-                        {% endblocktrans %}
-                    </p>
-                {% endif %}
-                {% if not member.canceled %}
-                    {% block button_cancel_membership %}
-                        <a href="{% url 'cancel-membership' %}" class="btn btn-outline-danger">
-                            {% trans "Mitgliedschaft künden" %}
-                        </a>
-                    {% endblock %}
-                {% endif %}
+    {% vocabulary "member_type" as v_member_type %}
+    {% if success %}
+        <div class="alert alert-success">{% trans "Personalien erfolgreich geändert" %}</div>
+    {% endif %}
+    {% include "transitions/_review_data_confirm.html" %}
+    {% if member.canceled %}
+        <div class="alert alert-warning">
+            {% blocktrans trimmed with cd=member.cancellation_date|date:"d.m.Y" %}
+                Deine {{ v_member_type }}schaft ist seit dem {{ cd }} gekündigt.
+            {% endblocktrans %}
+        </div>
+    {% endif %}
+    {% if not member.canceled and not member.inactive %}
+        <div class="alert alert-success">{% blocktrans %}Deine {{ v_member_type }}schaft ist aktiv.{% endblocktrans %}</div>
+    {% endif %}
+    <form method="post" class="mb-4">
+        {% load rotebeete %}
+        {% with form=memberform|disable_iban %}
+            {% crispy form %}
+        {% endwith %}
+    </form>
+    <div class="row mb-2">
+        <div class="offset-md-3 col-md-9">
+            <a href="{% url 'password' %}" class="btn btn-success">{% trans "Passwort ändern" %}</a>
+        </div>
+    </div>
+    {% if not member.canceled %}
+        <div class="row mb-2">
+            <div class="offset-md-3 col-md-9">
+                <a href="{% url 'cancel-membership' %}" class="btn btn-danger">{% trans "Mitgliedschaft künden" %}</a>
             </div>
         </div>
-    {% endblock %}
-    {% block documents %}
-        {% include "juntagrico/snippets/documents.html" %}
-    {% endblock %}
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

### `juntagrico/my/subscription/single.html`

#### Code diff

```diff
 {% load juntagrico.subscription %}
 {% block page_title %}
     {% vocabulary "subscription" as v_subscription %}
 {% endblock %}
 {% block content %}
     {% vocabulary "subscription" as v_subscription %}
@@ -32,9 +30,7 @@
         {# Subscription #}
         {% block part-list %}
             <div class="row mb-5 part-list">
                 <div class="col-md-9">
                     {% include 'juntagrico/my/subscription/snippets/part_list.html' with parts=subscription.parts.waiting_or_active %}
                 </div>
@@ -43,24 +39,17 @@
         {# Co-members #}
         {% block co-members %}
             <div class="row mb-5 co-members">
             </div>
         {% endblock %}
         {# Assignments #}
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

- Page title simplified to single line formatting
- Internal HTML formatting cleaned up (multi-line tags compressed)
- **Documents section replaced** with GLV (delivery contract) download link
- **Membership review confirmation widget** added
- Custom block nesting simplified

---

### `juntagrico/my/subscription/snippets/part_list.html`

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
- Indentation and formatting cleaned up throughout

---

## GENOSSENSCHAFTSANTEILE VERWALTEN

### `manage_shares.html`

#### Code diff

```diff
 {% block page_title %}
     {% vocabulary "share_pl" as v_share_pl %}
 {% endblock %}
 {% block content %}
     {% vocabulary "share_pl" as v_share_pl %}
     {% vocabulary "share" as v_share %}
     {% vocabulary "subscription" as v_subscription %}
-    {% block certificates %}
-        <h4>{% trans "Bescheinigung" %}</h4>
-        <p>
-            {% blocktrans %}Hier kannst du eine Bescheinigung über deine {{ v_share_pl }} der letzten Jahre herunterladen{% endblocktrans %}:
+    <h4>{% trans "Bescheinigung" %}</h4>
+    <p>
+        {% blocktrans %}Hier kannst du eine Bescheinigung über deine {{ v_share_pl }} der letzten Jahre herunterladen{% endblocktrans %}:
+    </p>
+    {% if certificate_years %}
+        <form action="{% url 'share-certificate' %}"
+              method="get"
+              class="form-inline">
+            <div class="form-group">
+                <select class="form-control" id="year_select" name="year">
+                    {% for year in certificate_years %}
+                        <option value="{{ year }}"
+                                {% if forloop.last %}selected="selected"{% endif %}>{{ year }}</option>
+                    {% endfor %}
+                </select>
+            </div>
+            <input type="submit"
+                   value="{% trans "Bescheinigung" %} {% trans "herunterladen" %}"
+                   class="btn btn-primary">
+        </form>
+    {% else %}
+        <p class="font-italic">
+            Keine {{ v_share_pl }} der vergangenen Jahre gefunden. Wenn du seit diesem Jahr {{ v_share_pl }} hälst, steht dir hier nächstes Jahr eine Bescheinigung zur Verfügung.
         </p>
-        {% if certificate_years %}
-            <form action="{% url 'share-certificate' %}" method="get" class="form-inline">
-                ...form elements...
-            </form>
-        {% else %}
-            <p class="font-italic">Keine {{ v_share_pl }}... gefunden</p>
         {% endif %}
-    {% endblock %}
-    {% block overview %}
         <h4>{% trans "Übersicht" %}</h4>
         {% if shares|length == 0 %}
             {% blocktrans %}Du hast noch keine {{ v_share_pl }}{% endblocktrans %}
         {% else %}
             <div>
                 <table id="filter-table" class="table">
                     <thead>
                         <tr>
                             <th></th>
                         </tr>
                     </thead>
                     <tbody>
                         {% for share in shares %}
                             <tr>
-                                            <a href="{% url 'cancel-membership' %}">...Mitgliedschaft kündigen...</a>
-                                        {% endif %}
-                                    {% elif share.cancelled_date is None %}
-                                        <a href="{% url 'share-cancel' share.id %}">{% trans "kündigen" %}</a>
+                                            <a href="{% url 'cancel-membership' %}">Mitgliedschaft kündigen</a>
+                                        {% endif %}
+                                    {% elif share.cancelled_date is None and share.paid_date is None %}
+                                        {% blocktrans %}Diese/s/r {{ v_share }} wurde noch nicht als bezahlt verbucht{% endblocktrans %}
+                                    {% elif ibanempty %}
+                                        <a href="{% url 'profile' %}">{% blocktrans %}Kann gekündigt werden, sobald eine IBAN hinterlegt ist{% endblocktrans %}</a>
+                                    {% elif share.cancelled_date is None and share.paid_date is not None %}
+                                        <a href="{% url 'share-cancel' share.id %}" class="btn btn-outline-danger"
+                                           onclick="return confirm('{% blocktrans %} Möchtest du diese/s/n {{ v_share }} verbindlich zum {{ next_membership_end_date }} kündigen? {% endblocktrans%}')">
+                                            {% trans "kündigen" %}
+                                        </a>
                                     {% endif %}
                                 </td>
                             </tr>
                         {% endfor %}
                     </tbody>
                 </table>
             </div>
         {% endif %}
-    {% endblock %}
-    {% block order %}
-        <h5>{% blocktrans %}{{ v_share_pl }} bestellen{% endblocktrans %}</h5>
-        <form method="post">
-            <input type="number" name="shares" ... />
-            <button type="submit">{% blocktrans %}Bestellen{% endblocktrans %}</button>
-        </form>
-    {% endblock %}
+    <script></script>
 {% endblock %}
```

#### User-facing changes

- **Share ordering form removed completely** — users can no longer order new shares from this page
- **Conditional cancellation logic added**:
  - If share is unpaid (`paid_date is None`): shows "noch nicht als bezahlt verbucht"
  - If no IBAN on file (`ibanempty`): shows message to add IBAN first
  - If share is paid and not cancelled: shows cancellation button with confirmation dialog
- HTML formatting simplified (block nesting removed, multiline tags condensed)

---

## GENOSSENSCHAFTSANTEILE — BESCHEINIGUNG

### `exports/share_certificate.html`

#### Code diff

```diff
 <!DOCTYPE html>
 <html lang="de">



         </style>
     <body>
         {% block content %}
-            <p class="member">
-                Name: {{ member.first_name }} {{ member.last_name }}<br>
-                {{ v_member }}-Nr.: {{ member.id }}
+            <p>
+                Name: {{ member.first_name }} {{ member.last_name }}
+                <br>
+                {{ v_member }}-Nr.: {{ member.share_set.first.number }}
             </p>
             <p class="main_text">
                 {% blocktrans with start_date=shares.0.creation_date|date:"d.m.Y" %}
```

#### User-facing changes

- **Member number on certificate now displays the share number** (`member.share_set.first.number`) instead of internal member ID
- **HTML formatting improved** with consistent indentation and whitespace
- **CSS formatting cleaned up** with proper spacing and alignment

---

## E-MAILS

### `mails/member/share_created.txt`

#### Code diff

```diff
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
-{% blocktrans %}Um die Arbeit der Buchhaltung zu erleichtern zahle bitte nur 1 {{ v_share }} auf einmal.
-Gib im Betreff die Systemnummer an und die Emailadresse der Halterin oder des Halters des/r {{ v_share }} an
-(dies ist vor allem wichtig wenn du diese/n/s {{ v_share }} für jemand anderen bezahlst){% endblocktrans %}
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
