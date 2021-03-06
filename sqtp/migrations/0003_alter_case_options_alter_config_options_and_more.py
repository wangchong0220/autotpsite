# Generated by Django 4.0.3 on 2022-03-26 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqtp', '0002_alter_project_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='case',
            options={'ordering': ['-create_time'], 'verbose_name': '测试用例表'},
        ),
        migrations.AlterModelOptions(
            name='config',
            options={'ordering': ['-create_time'], 'verbose_name': '配置表'},
        ),
        migrations.AlterModelOptions(
            name='environment',
            options={'ordering': ['-create_time'], 'verbose_name': '测试环境表'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-create_time'], 'verbose_name': '项目表'},
        ),
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ['-create_time'], 'verbose_name': '请求信息表'},
        ),
        migrations.AlterModelOptions(
            name='step',
            options={'ordering': ['-create_time'], 'verbose_name': '测试步骤表'},
        ),
    ]
