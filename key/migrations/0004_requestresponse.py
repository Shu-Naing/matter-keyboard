# Generated by Django 4.2.3 on 2023-07-11 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('key', '0003_checkdevice'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_text', models.TextField()),
                ('response_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
