# Generated by Django 2.0 on 2019-01-11 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0003_auto_20190111_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=32, verbose_name='作者'),
        ),
    ]
