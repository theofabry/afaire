# Generated by Django 3.0.6 on 2020-05-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20200530_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Réalisé'), (1, 'Non réalisé, indépendamment de ma volonté'), (2, 'Non réalisé, manque de temps/flemme'), (3, 'Echoué/abandonné'), (4, 'Réalisé après de nombreuses étapes'), (5, 'A faire'), (6, 'Avancé mais pas terminé'), (7, 'Fait sans avoir été prévu')], default=5),
        ),
    ]
