# Generated by Django 3.2.1 on 2021-08-19 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paperQ', '0006_auto_20210819_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='paperQ.person'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='paperQ.question'),
        ),
    ]
