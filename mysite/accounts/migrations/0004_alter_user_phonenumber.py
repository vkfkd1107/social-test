# Generated by Django 4.1.2 on 2022-10-05 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=11, verbose_name='전화번호'),
        ),
    ]
