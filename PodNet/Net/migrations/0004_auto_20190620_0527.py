# Generated by Django 2.2.2 on 2019-06-20 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Net', '0003_auto_20190618_0603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=50)),
                ('LastName', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='podcastfeed',
            name='feedurl',
            field=models.URLField(unique=True),
        ),
    ]