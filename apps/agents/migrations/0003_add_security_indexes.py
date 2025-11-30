# Generated migration for security fixes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0002_initial'),
    ]

    operations = [
        # Add indexes for foreign keys in agent_executions
        migrations.AddIndex(
            model_name='agentexecution',
            index=models.Index(fields=['prompt_used'], name='agent_exec_prompt_idx'),
        ),
        migrations.AddIndex(
            model_name='agentexecution',
            index=models.Index(fields=['provider'], name='agent_exec_provider_idx'),
        ),

        # Add indexes for foreign keys in agent_tasks
        migrations.AddIndex(
            model_name='agenttask',
            index=models.Index(fields=['assigned_to'], name='agent_task_assigned_idx'),
        ),
        migrations.AddIndex(
            model_name='agenttask',
            index=models.Index(fields=['parent_task'], name='agent_task_parent_idx'),
        ),

        # Add composite indexes for common queries
        migrations.AddIndex(
            model_name='agenttask',
            index=models.Index(fields=['status', 'priority'], name='agent_task_status_pri_idx'),
        ),
        migrations.AddIndex(
            model_name='agenttask',
            index=models.Index(fields=['agent_type', '-created_at'], name='agent_task_type_date_idx'),
        ),
        migrations.AddIndex(
            model_name='agentexecution',
            index=models.Index(fields=['success', '-created_at'], name='agent_exec_success_idx'),
        ),
    ]
