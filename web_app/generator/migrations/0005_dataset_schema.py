# Generated by Django 3.1 on 2020-08-18 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0004_auto_20200818_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='generator.schema'),
        ),
    ]
