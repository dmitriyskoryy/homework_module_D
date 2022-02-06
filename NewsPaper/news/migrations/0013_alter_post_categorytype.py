# Generated by Django 4.0.1 on 2022-02-05 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_alter_post_categorytype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categoryType',
            field=models.CharField(choices=[('NW', 'Новость'), ('AR', 'Статья')], default='NW', max_length=2),
        ),
    ]
