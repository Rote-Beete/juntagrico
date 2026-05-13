# Juntagrico Version Comparison

Comparison of template changes between Juntagrico 2.0.7 and latest version.

**Summary:** 4 templates have changes.

---
## ADMIN
### `juntagrico/menu/admin/lists.html`

```diff
@@ -1,10 +1,41 @@
 {% load juntagrico.config %}
 {% load i18n %}
 {% if perms.juntagrico.can_view_lists or perms.juntagrico.can_generate_lists %}
     <li class="nav-item">
-        <a class="nav-link" href="{% url 'lists' %}">
+        <a class="nav-link" data-toggle="collapse" href="#lists">
             {% trans "Listen" %}
+            <i class="fas fa-angle-right">
+            </i>
         </a>
+        <div class="collapse {% if 'manage-list' in request.resolver_match.url_name %} show{% endif %}" id="lists">
+            <ul class="nav flex-column admin-menu subadmin-menu">
+                {% block sub %}
+                    {% if perms.juntagrico.can_generate_lists %}
+                        <li class="nav-item">
+                            <a class="nav-link" href="{% url 'manage-list' %}">
+                                {% trans "Erzeugen" %}
+                            </a>
+                        </li>
+                    {% endif %}
+                    {% if perms.juntagrico.can_view_lists %}
+                        <li class="nav-item">
+                            <a class="nav-link" href="{% url 'lists-depot-amountoverview' %}">
+                                {% trans "Mengen Übersicht" %}
+                            </a>
+                        </li>
+                        <li class="nav-item">
+                            <a class="nav-link" href="{% url 'lists-depotlist' %}">
+                                {% vocabulary "depot" %}-{% trans "Listen" %}
+                            </a>
+                        </li>
+                        <li class="nav-item">
+                            <a class="nav-link" href="{% url 'lists-depot-overview' %}">
+                                {% vocabulary "depot" %} {% trans "Übersicht" %}
+                            </a>
+                        </li>
+                    {% endif %}
+                {% endblock %}
+            </ul>
+        </div>
     </li>
-{% endif %}
+{% endif %}
```

---
## MITGLIEDSCHAFT
### `juntagrico/my/subscription/snippets/part_list.html`
```diff
@@ -14,92 +14,61 @@
         </thead>
         <tbody>
         {% for part in parts.sorted %}
-            {% with remaining=part.remaining_trial_days %}
-                <tr>
-                    <td>
-                        {{ part }}
-                        {% if part.is_trial %}<span class="badge badge-info">{% trans "Probe" %}</span>{% endif %}
-                    </td>
-                    <td>
-                        {% if remaining > 0 %}
-                            {{ part.state_text }}
-                            <div>
-                                {% blocktrans trimmed count remaining=remaining %}
-                                    Noch {{ remaining }} Tag
-                                {% plural %}
-                                    Noch {{ remaining }} Tage
-                                {% endblocktrans %}
-                            </div>
-                        {% elif remaining <= 0 %}
-                            <span class="badge badge-danger">{% trans "abgelaufen" %}</span>
-                        {% else %}
-                            {{ part.state_text }}
+            <tr>
+                <td>{{ part }}</td>
+                <td>{{ part.state_text }}</td>
+                <td>
+                    {% if part.cancellation_date %}
+                        {% blocktrans trimmed with cd=part.cancellation_date %}
+                            Gekündigt am {{ cd }}
+                        {% endblocktrans %}
+                        {% if part.deactivation_date %}
+                            <br>
+                            {% blocktrans trimmed with dd=part.deactivation_date %}
+                                Noch aktiv bis am {{ dd }}
+                            {% endblocktrans %}
                         {% endif %}
-                    </td>
-                    <td>
-                        {% if part.cancellation_date %}
-                            {% blocktrans trimmed with cd=part.cancellation_date %}
-                                Gekündigt am {{ cd }}
-                            {% endblocktrans %}
-                            {% if part.deactivation_date %}
+                    {% else %}
+                        {% with ad=part.activation_date %}
+                            {% if part.active %}
+                                {% blocktrans %}Aktiv seit {{ ad }}{% endblocktrans %}
                                 <br>
-                                {% blocktrans trimmed with dd=part.deactivation_date %}
-                                    Noch aktiv bis am {{ dd }}
-                                {% endblocktrans %}
+                            {% elif ad %}
+                                {% blocktrans %}Wird aktiv am {{ ad }}{% endblocktrans %}
+                                <br>
                             {% endif %}
-                        {% else %}
-                            {% with ad=part.activation_date %}
-                                {% if part.active %}
-                                    {% if remaining > 0 %}
-                                        {% blocktrans trimmed %}
-                                            Aktiv seit {{ ad }}
-                                        {% endblocktrans %}
-                                        <br>
-                                    {% endif %}
-                                {% elif ad %}
-                                    {% blocktrans trimmed %}
-                                        Wird aktiv am {{ ad }}
-                                    {% endblocktrans %}
-                                    <br>
+                        {% endwith %}
+                        {% if subscription.primary_member == member %}
+                            {% if part.is_extra %}
+                                {% if part.state != 'canceled' and  part.state != 'inactive' %}
+                                    <a href="{% url 'part-cancel' part.id subscription.id %}" class="btn btn-danger"
+                                    onclick="return confirm('{% trans "Bist du sicher, dass du dieses Zusatzabo kündigen möchtest?" %}')">
+                                        {% trans "kündigen" %}
+                                    </a>
                                 {% endif %}
-                            {% endwith %}
-                            {% if subscription.primary_member == member %}
-                                {% if part.is_trial %}
-                                    {% if not part.follow_up_parts.exists %}
-                                        <div>{% trans "Willst du weitermachen?" %}</div>
-                                        {% include "./buttons/trial.html" %}
-                                    {% endif %}
-                                {% elif part.is_extra %}
-                                    {% if part.state != 'canceled' and  part.state != 'inactive' %}
-                                        <a href="{% url 'part-cancel' part.id %}" class="btn btn-danger"
-                                        onclick="return confirm('{% trans "Bist du sicher, dass du dieses Zusatzabo kündigen möchtest?" %}')">
-                                            {% trans "kündigen" %}
+                            {% else %}
+                                {% if can_change_part %}
+                                    <a href="{% url 'part-change' part.id %}" class="btn btn-primary">
+                                        {% trans "ändern" %}
+                                    </a>
+                                {% endif %}
+                                {% if part.subscription.future_parts.is_normal.count == 1 %}
+                                    {% if part.subscription.state != 'canceled' and  part.subscription.state != 'inactive' %}
+                                        <a href="{% url 'sub-cancel' subscription.id %}" class="btn btn-danger">
+                                            {% blocktrans %}{{ v_subscription }} komplett künden{% endblocktrans %}
                                         </a>
                                     {% endif %}
-                                {% else %}
-                                    {% if can_change_part %}
-                                        <a href="{% url 'part-change' part.id %}" class="btn btn-primary">
-                                            {% trans "ändern" %}
-                                        </a>
-                                    {% endif %}
-                                    {% if part.subscription.future_parts.is_normal.count == 1 %}
-                                        {% if part.subscription.state != 'canceled' and  part.subscription.state != 'inactive' %}
-                                            <a href="{% url 'sub-cancel' subscription.id %}" class="btn btn-danger">
-                                                {% blocktrans %}{{ v_subscription }} komplett künden{% endblocktrans %}
-                                            </a>
-                                        {% endif %}
-                                    {% elif part.subscription.future_parts.is_normal.count > 1 %}
-                                        <a href="{% url 'part-cancel' part.id %}" class="btn btn-danger"
-                                        onclick="return confirm('{% trans "Bist du sicher, dass du diesen Bestandteil kündigen möchtest?" %}')">
-                                            {% trans "kündigen" %}
-                                        </a>
-                                    {% endif %}
+                                {% elif part.subscription.future_parts.is_normal.count > 1 %}
+                                    <a href="{% url 'part-cancel' part.id subscription.id %}" class="btn btn-danger"
+                                    onclick="return confirm('{% trans "Bist du sicher, dass du diesen Bestandteil kündigen möchtest?" %}')">
+                                        {% trans "kündigen" %}
+                                    </a>
                                 {% endif %}
                             {% endif %}
                         {% endif %}
-                    </td>
-                </tr>
-            {% endwith %}
+                    {% endif %}
+                </td>
+            </tr>
         {% endfor %}
         </tbody>
     </table>
@@ -113,7 +82,7 @@
 {% if extra_sub_info.strip %}
     <a href="{{ extra_sub_info }}" target="_blank">
         {% trans "Infos zu den Zusatz-Abos" %}
-        <i class="bi bi-box-arrow-up-right small"></i>
+        <i class="fa-solid fa-arrow-up-right-from-square small"></i>
     </a>
 {% endif %}
```

---
## GENOSSENSCHAFTSANTEILE VERWALTEN
### `manage_shares.html`
```diff
@@ -25,7 +25,7 @@
                         <option value="{{ year }}"{% if forloop.last %} selected="selected"{% endif %}>{{ year }}</option>
                         {% endfor %}
                     </select>
-                    <input type="submit" value="{% trans "Bescheinigung herunterladen" %}" class="btn btn-primary">
+                    <input type="submit" value="{% trans "Bescheinigung" %} {% trans "herunterladen" %}" class="btn btn-primary">
                 </div>
             </form>
         {% else %}
@@ -119,7 +119,6 @@
 {% block scripts %}
     <script type="text/javascript" src="{% static 'juntagrico/external/bootstrap-input-spinner.js' %}">
     </script>
-    <script type="text/javascript">
-        $("input[type='number']").inputSpinner();
+    <script type="text/javascript" src="{% static 'juntagrico/external/require.min.js' %}" data-main="{% static 'juntagrico/js/initChangeExtra.js' %}">
     </script>
 {% endblock %}
```

---
## GENOSSENSCHAFTSANTEILE — BESCHEINIGUNG
### `exports/share_certificate.html`
```diff
@@ -93,7 +93,7 @@
 {{ member.addr_zipcode }} {{ member.addr_location }}
 </p>
 <p class="letter_date">{{ cert_date|date:"DATE_FORMAT" }}</p>
-<p class="subject"><b>{% blocktrans %}Bescheinigung {{ v_share_pl }}{% endblocktrans %}</b></p>
+<p class="subject"><b>{% trans "Bescheinigung" %} {{ v_share_pl }}</b></p>
 <p class="member">
     Name: {{ member.first_name }} {{ member.last_name }}<br>
```

---