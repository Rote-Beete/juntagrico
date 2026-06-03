server:
`containers-ng`

Die Daten sind hier:

`/var/lib/rotebeete-staging/`

Juntagrico 1.7.10: Branch v1

Juntagrico 2.0.7: Branch v2

`juntagrico/entity/subtypes.py` wurde stark überarbeitet. `SubscriptionSize` gibt es nicht mehr. Die entsprechenden Stellen wurden angepasst. 

Die Migrationen wurden stark squashed. `biddings` App kommt damit nicht zu recht. Deswegen wurden die `biddings` überarbeitet und die alten Migrationen entfernt. Die Umstellung wird deswegen zu Problemen in der alten Datenbank führen. Am sichersten ist:

1. Die Tabellen von `biddings` vor der Umstellung auf Version 2.0.7 komplett zu entfernen (es gibt ein Make Kammando dafür). Auf dem Server bei Kartoffel und containers-ng in `/tmp` gibt es schon ein dump file (Stand 03.06.26) von production bereits ohne biddings (`rb-production-20260603-without-biddings.dump`)
2. Erst dann mit Version 2 migrieren. 


Für alle Fälle eine cheat sheet:

## create a dump from production db

```
podman exec rotebeete-production-postgres pg_dump -Fc -U rotebeete -d rotebeete > /tmp/rb-production-20260603.dump
```

## replace db in staging (and later production)

```
podman exec -it rotebeete-staging-postgres psql -U rotebeete -d postgres -c "DROP DATABASE rotebeete;"
podman exec -it rotebeete-staging-postgres psql -U rotebeete -d postgres -c "CREATE DATABASE rotebeete;"
podman exec -i rotebeete-staging-postgres pg_restore -U rotebeete -d rotebeete --no-owner --no-privileges --disable-triggers < /tmp/rb-production-20260603.dump
```

Während Entwicklung kann man auch die entsprechenden Make Kommandos verwenden.



Noch zu Tun:

1. Umzug Repo (public) zu gitlab oder eine eigene Space auf `git@git.hack-hro.de`
2. Eventuell: 
    1. Wieder das Anmeldeformular aktivieren (erst mit Lou besprechen)
    2. Die Benutzer sollten selbst die Verteilerstation nicht wechseln können (auch erst mit Lou besprechen)
3. Das Upgrade auf Juntagrico 2.0.7:
    1. Erst alle Aufgaben abschließen, die aktuell noch mit den Beitragsrunden zu tun haben, damit die jetzigen Daten aus der DB entfernt werden können. (Ansonsten müsste man z.B. die Daten als JSON exportieren, anpassen und wieder importieren. Viel zu viel Arbeit...)
    2. Die Staging-Seite zum Laufen bringen (mit Konni)
    3. Alles mit Lou durchgehen (`ROTEBEETE-JUNTAGRICO-CHANGES.md` kann helfen muss aber auch selbst aktualisiert werden.)
    4. `REAMDE.md` aktualisieren.
    5. Wenn alles okay ist, einen tag mit der neuen Version (z.B. v2.0.0) anlegen und das neue Production Image erstellen lassen. (Die CI müsste es können, Konni weiß am besten, wie es geht.)
    6. Die Produktionsdatenbank erst wie oben beschrieben für die Umstellung auf v2 vorbereiten.
    7. Die `.env` Datei, wie in README beschrieben anpassen (z.B. die Email Einstellungen etc.)
    8. Production doployen.
4. Das Deployment von wiki und juntagrico abgeben (mit Lou besprechen. Er weiß schon jemanden)

DAAAANNNNNKKKKEEEEEE!
