# Generated by Django 4.2.6 on 2023-11-02 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='aid',
            new_name='answer_id',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='qid',
            new_name='question_id',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='uid',
            new_name='user_id',
        ),
    ]
