# Generated by Django 3.1.1 on 2020-09-10 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0005_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
