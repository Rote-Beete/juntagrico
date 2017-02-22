# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 19:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_ortoloco', '0016_auto_20161014_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraAbo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('activation_date', models.DateField(blank=True, null=True, verbose_name=b'Aktivierungssdatum')),
                ('deactivation_date', models.DateField(blank=True, null=True, verbose_name=b'Deaktivierungssdatum')),
                ('abo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='extra_abo_set', to='my_ortoloco.Abo')),
            ],
            options={
                'verbose_name': 'Zusatz-Abo',
                'verbose_name_plural': 'Zusatz-Abos',
            },
        ),
        migrations.AlterModelOptions(
            name='extraabotype',
            options={'verbose_name': 'Zusatz-Abo-Typ', 'verbose_name_plural': 'Zusatz-Abo-Typen'},
        ),
        migrations.AddField(
            model_name='extraabo',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='type', to='my_ortoloco.ExtraAboType'),
        ),
    ]