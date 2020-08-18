# Generated by Django 3.1 on 2020-08-17 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0002_column_schema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('processing', 'Processing'), ('ready', 'Ready'), ('error', 'Error')], default='created', max_length=32),
        ),
    ]
