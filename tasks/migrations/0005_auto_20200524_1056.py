# Generated by Django 3.0.6 on 2020-05-24 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20200523_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Réalisé'), (1, 'Non réalisé, indépendamment de ma volonté'), (2, 'Non réalisé, manque de temps/flemme'), (3, 'Echoué/abandonné'), (4, 'Réalisé après de nombreuses étapes'), (5, 'A faire')], default=5),
        ),
    ]
