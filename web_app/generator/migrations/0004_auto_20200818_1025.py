# Generated by Django 3.1 on 2020-08-18 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0003_auto_20200817_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='column', to='generator.schema'),
        ),
    ]
