# Generated by Django 4.2 on 2023-05-31 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_shoppingcart_favourite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='media/', verbose_name='Картинка'),
        ),
    ]
