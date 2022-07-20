# Generated by Django 3.2.5 on 2022-07-20 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('password', models.TextField()),
                ('available', models.BooleanField(default=True)),
            ],
        ),
    ]