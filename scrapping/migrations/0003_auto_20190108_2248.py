# Generated by Django 2.1.5 on 2019-01-08 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping', '0002_auto_20190106_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultproperty',
            name='price',
            field=models.CharField(default='Price ERROR', max_length=20),
        ),
    ]
