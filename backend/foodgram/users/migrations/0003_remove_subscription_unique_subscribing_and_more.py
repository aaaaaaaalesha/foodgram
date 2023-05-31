# Generated by Django 4.2 on 2023-05-29 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_subscription_author'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscription',
            name='unique_subscribing',
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_subscription'),
        ),
    ]
