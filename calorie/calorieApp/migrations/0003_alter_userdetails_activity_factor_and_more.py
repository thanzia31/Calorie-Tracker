# Generated by Django 4.1.6 on 2023-09-07 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calorieApp', '0002_additems_meal_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='activity_factor',
            field=models.CharField(choices=[('1', 'Little/No Exercise'), ('2', 'light exercise/sports 1-3 days per week'), ('3', 'moderate exercise/sports 3-5 days per week'), ('4', 'hard exercise/sports 6-7 days per week'), ('5', 'very hard exercise/sports & a physical job')], max_length=30),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
