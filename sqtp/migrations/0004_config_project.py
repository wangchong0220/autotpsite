# Generated by Django 4.0.3 on 2022-03-26 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sqtp', '0003_alter_case_options_alter_config_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sqtp.project'),
        ),
    ]
