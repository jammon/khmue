# Generated by Django 4.0 on 2021-12-30 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "geraete",
            "0004_employee_instructor_for_professionalgroup_devices_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="instruction",
            name="device",
        ),
        migrations.RemoveField(
            model_name="instruction",
            name="is_primary",
        ),
        migrations.AddField(
            model_name="employee",
            name="title",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="Titel"
            ),
        ),
        migrations.AddField(
            model_name="instruction",
            name="devices",
            field=models.ManyToManyField(
                related_name="instructions", to="geraete.Device"
            ),
        ),
    ]
