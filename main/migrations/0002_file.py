# Generated by Django 5.1.2 on 2024-10-29 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.FileField(upload_to='files/')),
                ('description', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='main.lesson')),
            ],
            options={
                'verbose_name': 'Dars uchun fayl',
                'verbose_name_plural': 'Dars uchun fayllar',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]