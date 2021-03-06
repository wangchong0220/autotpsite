# Generated by Django 4.0.3 on 2022-03-27 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sqtp', '0005_alter_project_options_remove_project_members_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='config',
            options={'ordering': ['-create_time'], 'verbose_name': '用例配置表'},
        ),
        migrations.AlterModelOptions(
            name='environment',
            options={'ordering': ['id'], 'verbose_name': '测试环境'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['id'], 'verbose_name': '项目表'},
        ),
        migrations.RemoveField(
            model_name='case',
            name='update_by',
        ),
        migrations.RemoveField(
            model_name='config',
            name='update_by',
        ),
        migrations.RemoveField(
            model_name='environment',
            name='update_by',
        ),
        migrations.RemoveField(
            model_name='project',
            name='update_by',
        ),
        migrations.RemoveField(
            model_name='request',
            name='update_by',
        ),
        migrations.RemoveField(
            model_name='step',
            name='update_by',
        ),
        migrations.AddField(
            model_name='case',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='config',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='environment',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='request',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='step',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AlterField(
            model_name='case',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='case',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='config',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='config',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='environment',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='environment',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='environment',
            name='ip',
            field=models.GenericIPAddressField(default='127.0.0.1', verbose_name='IP地址'),
        ),
        migrations.AlterField(
            model_name='environment',
            name='os',
            field=models.SmallIntegerField(choices=[(0, 'windows'), (1, 'Linux')], default=1, verbose_name='服务器操作系统'),
        ),
        migrations.AlterField(
            model_name='environment',
            name='port',
            field=models.PositiveSmallIntegerField(default=80, verbose_name='端口号'),
        ),
        migrations.AlterField(
            model_name='project',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='project_admin', to=settings.AUTH_USER_MODEL, verbose_name='项目管理员'),
        ),
        migrations.AlterField(
            model_name='project',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='project',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(related_name='project_members', to=settings.AUTH_USER_MODEL, verbose_name='项目成员'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='项目名称'),
        ),
        migrations.AlterField(
            model_name='project',
            name='version',
            field=models.CharField(default='v0.1', max_length=32, verbose_name='项目版本'),
        ),
        migrations.AlterField(
            model_name='request',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='request',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='request',
            name='step',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testrequest', to='sqtp.step'),
        ),
        migrations.AlterField(
            model_name='step',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='step',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='user',
            name='realname',
            field=models.CharField(max_length=32, verbose_name='真实姓名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.SmallIntegerField(choices=[(0, '开发'), (1, '测试'), (2, '运维'), (3, '项目经理')], default=1, verbose_name='用例类型'),
        ),
    ]
