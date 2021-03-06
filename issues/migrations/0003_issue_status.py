# Generated by Django 3.0.3 on 2020-02-26 15:04

from django.db import migrations, models
import issues.models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_auto_20200226_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('CREATED', 'CREATED'), ('OPEN', 'OPEN'), ('ASSIGNED', 'ASSIGNED'), ('CLOSED', 'CLOSED')], default=issues.models.IssueStatusChoices['CREATED'], max_length=50),
        ),
    ]
