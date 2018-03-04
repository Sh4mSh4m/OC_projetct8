# Generated by Django 2.0.2 on 2018-02-25 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_product', models.CharField(max_length=200)),
                ('brand', models.CharField(max_length=200)),
                ('quantity', models.CharField(max_length=20)),
                ('nutrition', models.CharField(max_length=2)),
                ('description', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('code', models.IntegerField()),
            ],
        ),
    ]
