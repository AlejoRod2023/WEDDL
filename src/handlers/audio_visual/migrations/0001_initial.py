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
            name='AudioVisualRequest',
            fields=[
                ('baserequest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='download.baserequest')),
                ('format_selection', models.CharField(max_length=50, verbose_name='format selection')),
                ('output', models.CharField(max_length=100, verbose_name='output')),
            ],
            options={
                'db_table': 'audio_visual_request',
            },
            bases=('download.baserequest',),
        ),
    ]
