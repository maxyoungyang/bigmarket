# Generated by Django 2.2.5 on 2019-09-14 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('marketing', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='agent_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.AgentGroup', verbose_name='所属代理分组'),
        ),
    ]
