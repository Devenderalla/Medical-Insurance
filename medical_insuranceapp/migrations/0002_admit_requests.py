# Generated by Django 3.2.12 on 2024-07-18 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical_insuranceapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admit_Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('vendor_email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=100)),
                ('discription', models.CharField(max_length=100)),
                ('hospital_name', models.CharField(max_length=100)),
                ('reasonfor_admit', models.CharField(max_length=100)),
                ('admit_date', models.DateField()),
                ('booking_date', models.DateTimeField(auto_now=True)),
                ('bstatus', models.CharField(default='Pending', max_length=100)),
                ('hospitals', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical_insuranceapp.hospitals')),
            ],
            options={
                'db_table': 'Admit_Requests',
            },
        ),
    ]
