# Generated by Django 4.0 on 2022-03-26 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_blood_customuser_city_customuser_role_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blood',
            name='group',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Blood Group'),
        ),
    ]
