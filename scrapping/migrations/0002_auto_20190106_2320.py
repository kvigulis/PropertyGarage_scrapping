# Generated by Django 2.1.5 on 2019-01-06 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultproperty',
            name='URL',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='resultproperty',
            name='price',
            field=models.FloatField(blank=True, db_column='result:price', default=0, null=True),
        ),
        migrations.AlterField(
            model_name='resultproperty',
            name='property_id',
            field=models.IntegerField(blank=True, db_column='result:id', default=0, null=True),
        ),
    ]