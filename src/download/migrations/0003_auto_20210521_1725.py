# Generated by Django 3.2.3 on 2021-05-21 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0002_baserequest_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='baserequest',
            name='compressed_at',
            field=models.DateTimeField(null=True, verbose_name='compressed at'),
        ),
        migrations.AddField(
            model_name='baserequest',
            name='start_compressing_at',
            field=models.DateTimeField(null=True, verbose_name='start compressing at'),
        ),
    ]