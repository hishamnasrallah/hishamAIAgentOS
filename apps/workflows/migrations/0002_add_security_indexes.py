# Generated migration for workflow security fixes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0001_initial'),
    ]

    operations = [
        # Add indexes for foreign keys
        migrations.AddIndex(
            model_name='workflowstep',
            index=models.Index(fields=['agent_task'], name='workflow_step_task_idx'),
        ),

        # Add composite indexes for common queries
        migrations.AddIndex(
            model_name='workflow',
            index=models.Index(fields=['status', '-created_at'], name='workflow_status_date_idx'),
        ),
    ]
