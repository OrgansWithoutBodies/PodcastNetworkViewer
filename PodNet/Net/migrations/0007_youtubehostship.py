# Generated by Django 2.2.2 on 2019-06-20 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Net', '0006_youtubechannel_channelname'),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeHostship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Channel', models.ForeignKey(null=True, on_delete='set_null', to='Net.YoutubeChannel')),
                ('Person', models.ForeignKey(null=True, on_delete='set_null', to='Net.Person')),
            ],
        ),
    ]