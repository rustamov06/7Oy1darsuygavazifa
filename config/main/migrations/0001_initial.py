# Generated by Django 5.1.6 on 2025-02-25 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Brand nomi ')),
            ],
            options={
                'verbose_name': 'Brand ',
                'verbose_name_plural': 'Brandlar ',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100, verbose_name='Moshinaning rangi')),
            ],
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_name', models.CharField(max_length=200, verbose_name='Model nomi ')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='new/photos/', verbose_name='Moshinani rasmi')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Ishlab chirqarilgan vaqti')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Narxi')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.brands', verbose_name='Brand nomi')),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.color')),
            ],
            options={
                'verbose_name': 'Moshina ',
                'verbose_name_plural': 'Moshinalar ',
            },
        ),
    ]
