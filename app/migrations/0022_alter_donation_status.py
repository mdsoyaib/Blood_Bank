# Generated by Django 4.0 on 2022-08-27 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Canceled', 'Canceled'), ('Collected', 'Collected'), ('Expired', 'Expired')], default='Pending', max_length=255, null=True),
        ),
    ]
