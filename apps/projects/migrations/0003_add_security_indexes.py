# Generated migration for project security fixes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_initial'),
    ]

    operations = [
        # Add indexes for foreign keys
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['owner'], name='project_owner_idx'),
        ),
        migrations.AddIndex(
            model_name='projectmember',
            index=models.Index(fields=['user'], name='project_member_user_idx'),
        ),
    ]
