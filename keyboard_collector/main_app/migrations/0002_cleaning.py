# Generated by Django 4.0.6 on 2022-07-19 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cleaning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('S', 'Switches'), ('K', 'Keycaps'), ('B', 'Body')], default='S', max_length=1)),
                ('keyboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.keyboard')),
            ],
        ),
    ]