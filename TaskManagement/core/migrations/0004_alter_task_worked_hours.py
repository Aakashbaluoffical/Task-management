# Generated by Django 5.2.1 on 2025-05-24 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_groups_user_is_staff_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='worked_hours',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
