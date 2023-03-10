# Generated by Django 4.1.2 on 2022-12-20 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_entities_account_names_entity'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.entities'),
        ),
        migrations.AlterField(
            model_name='entities',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
