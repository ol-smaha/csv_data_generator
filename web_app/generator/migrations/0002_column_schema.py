# Generated by Django 3.1 on 2020-08-14 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='generator.schema'),
        ),
    ]