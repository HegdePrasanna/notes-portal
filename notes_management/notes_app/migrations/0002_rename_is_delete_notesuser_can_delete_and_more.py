# Generated by Django 4.2.10 on 2024-02-20 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notesuser',
            old_name='is_delete',
            new_name='can_delete',
        ),
        migrations.RenameField(
            model_name='notesuser',
            old_name='is_edit',
            new_name='can_edit',
        ),
        migrations.RenameField(
            model_name='notesuser',
            old_name='is_read',
            new_name='can_read',
        ),
    ]
