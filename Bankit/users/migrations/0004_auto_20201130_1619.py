# Generated by Django 3.1.3 on 2020-12-01 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_history_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='user_id',
        ),
        migrations.AddField(
            model_name='history',
            name='account_number',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='users.account'),
            preserve_default=False,
        ),
    ]
