# Generated by Django 3.2.14 on 2022-07-20 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userrole'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userrole',
            constraint=models.UniqueConstraint(fields=('user', 'role'), name='unique_user_roles'),
        ),
    ]
