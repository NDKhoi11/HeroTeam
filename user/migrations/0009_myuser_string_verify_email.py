# Generated by Django 3.0.4 on 2020-04-02 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20200325_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='string_verify_email',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
