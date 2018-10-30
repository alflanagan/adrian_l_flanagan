# Generated by Django 2.1.2 on 2018-10-30 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0004_rename_techused'),
    ]

    operations = [
        migrations.AddField(
            model_name='softwareproject',
            name='fork_count',
            field=models.IntegerField(default=0, help_text='Count of forks of this repo'),
        ),
        migrations.AddField(
            model_name='softwareproject',
            name='is_fork',
            field=models.BooleanField(default=False, help_text='Is the repo a fork of a parent repo?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='softwareproject',
            name='issue_count',
            field=models.IntegerField(default=0, help_text='Count of open github issues'),
        ),
        migrations.AddField(
            model_name='softwareproject',
            name='last_update',
            field=models.DateTimeField(help_text='Date/time of last push', null=True),
        ),
        migrations.AddField(
            model_name='softwareproject',
            name='license',
            field=models.CharField(default='none', help_text='The software license for the project', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='softwareproject',
            name='parent',
            field=models.CharField(blank=True, help_text='Name of the parent repo, if any', max_length=250),
        ),
        migrations.AddField(
            model_name='softwareproject',
            name='primary_language',
            field=models.ForeignKey(blank=True, help_text='Primary language', null=True, on_delete=django.db.models.deletion.PROTECT, to='software.Technology'),
        ),
        migrations.AddField(
            model_name='softwareproject',
            name='stargazers',
            field=models.IntegerField(default=0, help_text='Count of users who starred this project'),
        ),
        migrations.AddField(
            model_name='softwareproject',
            name='watchers',
            field=models.IntegerField(default=0, help_text='Count of users watching this project'),
        ),
        migrations.AlterField(
            model_name='softwareproject',
            name='github_repo',
            field=models.CharField(blank=True, help_text='repo name in github (between "owner/" and ".git" in URL)', max_length=50),
        ),
    ]