# Generated by Django 3.0.6 on 2020-05-29 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20200524_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Réalisé'), (1, 'Non réalisé, indépendamment de ma volonté'), (2, 'Non réalisé, manque de temps/flemme'), (3, 'Echoué/abandonné'), (4, 'Réalisé après de nombreuses étapes'), (5, 'A faire'), (6, 'Avancé mais pas terminé')], default=5),
        ),
    ]