# Generated by Django 3.2 on 2021-04-10 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectRequest',
            fields=[
                ('baserequest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='download.baserequest')),
            ],
            options={
                'db_table': 'direct_request',
            },
            bases=('download.baserequest',),
        ),
    ]
