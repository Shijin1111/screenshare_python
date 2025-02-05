# Generated by Django 5.1.4 on 2025-02-04 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_problem_expected_cpp_signature_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='expected_cpp_signature',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='expected_java_signature',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='expected_python_signature',
        ),
        migrations.AddField(
            model_name='problem',
            name='cpp_signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='java_signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='main_cpp',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='main_java',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='main_python',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='prefix_cpp',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='prefix_java',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='prefix_python',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='python_signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='constraints',
            field=models.TextField(blank=True, null=True),
        ),
    ]
