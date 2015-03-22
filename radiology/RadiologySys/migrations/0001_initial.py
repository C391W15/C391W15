# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Family_doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pacs_images',
            fields=[
                ('image_id', models.IntegerField(primary_key=True, serialize=False)),
                ('thumbnail', models.ImageField(blank=True, upload_to='thumbnails')),
                ('regular_size', models.ImageField(blank=True, upload_to='regular_size')),
                ('full_size', models.ImageField(blank=True, upload_to='full_size')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('person_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=24)),
                ('last_name', models.CharField(max_length=24)),
                ('address', models.CharField(max_length=128)),
                ('email', models.CharField(unique=True, max_length=128)),
                ('phone', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Radiology_record',
            fields=[
                ('record_id', models.IntegerField(primary_key=True, serialize=False)),
                ('test_type', models.CharField(max_length=24)),
                ('prescribing_date', models.DateField()),
                ('test_date', models.DateField()),
                ('diagnosis', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('doctor_id', models.ForeignKey(to='RadiologySys.Persons', related_name='person_idDocRec')),
                ('patient_id', models.ForeignKey(to='RadiologySys.Persons', related_name='person_idPatRec')),
                ('radiologist_id', models.ForeignKey(to='RadiologySys.Persons', related_name='person_idRadRec')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('classType', models.CharField(choices=[('a', 'Admin'), ('p', 'Patient'), ('d', 'Doctor'), ('r', 'Radiologist')], max_length=1)),
                ('date_registered', models.DateField()),
                ('person_id', models.ForeignKey(to='RadiologySys.Persons')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pacs_images',
            name='record_id',
            field=models.ForeignKey(to='RadiologySys.Radiology_record', related_name='record_idPic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family_doctor',
            name='doctor_id',
            field=models.ForeignKey(to='RadiologySys.Persons', related_name='person_idDoc'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family_doctor',
            name='patient_id',
            field=models.ForeignKey(to='RadiologySys.Persons', related_name='person_idPat'),
            preserve_default=True,
        ),
    ]
