# Generated by Django 3.0.6 on 2020-05-23 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20200514_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Réalisé'), (1, 'Non réalisé, indépendamment de ma volonté'), (2, 'Non réalisé, manque de temps/flemme'), (3, 'Echoué/abandonné'), (4, 'Réalisé après de nombreuses étapes')], null=True),
        ),
    ]
