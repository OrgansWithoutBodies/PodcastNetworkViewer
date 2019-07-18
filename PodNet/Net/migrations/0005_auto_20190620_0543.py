# Generated by Django 2.2.2 on 2019-06-20 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Net', '0004_auto_20190620_0527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Hostship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='Guest',
        ),
        migrations.DeleteModel(
            name='Host',
        ),
        migrations.DeleteModel(
            name='Owner',
        ),
        migrations.DeleteModel(
            name='Speaker',
        ),
        migrations.DeleteModel(
            name='YoutubeHost',
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name_plural': 'People'},
        ),
        migrations.AddField(
            model_name='hostship',
            name='Person',
            field=models.ForeignKey(blank=True, null=True, on_delete='set_null', to='Net.Person'),
        ),
        migrations.AddField(
            model_name='hostship',
            name='Pod',
            field=models.ForeignKey(blank=True, null=True, on_delete='set_null', to='Net.Podcast'),
        ),
    ]
