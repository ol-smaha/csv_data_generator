# Generated by Django 3.1 on 2020-08-18 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0005_dataset_schema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('ready', 'Ready')], default='processing', max_length=32),
        ),
    ]
