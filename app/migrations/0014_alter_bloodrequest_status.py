# Generated by Django 4.0 on 2022-03-29 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_bloodrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodrequest',
            name='status',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Approved', max_length=20, null=True),
        ),
    ]
