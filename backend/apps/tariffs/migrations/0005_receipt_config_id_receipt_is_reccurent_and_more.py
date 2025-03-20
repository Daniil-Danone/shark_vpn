# Generated by Django 5.1.2 on 2025-03-20 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tariffs', '0004_alter_receipt_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='config_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='ID конфига'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='is_reccurent',
            field=models.BooleanField(default=False, verbose_name='Рекуррентный платёж'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='message_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='ID сообщения'),
        ),
    ]
