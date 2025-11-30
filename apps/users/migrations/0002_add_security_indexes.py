# Generated migration for user security fixes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('auth', '__latest__'),
    ]

    operations = [
        # Add indexes for auth tables foreign keys
        migrations.RunSQL(
            sql="""
                CREATE INDEX IF NOT EXISTS users_groups_group_id_idx
                ON users_groups(group_id);

                CREATE INDEX IF NOT EXISTS users_user_permissions_permission_id_idx
                ON users_user_permissions(permission_id);

                CREATE INDEX IF NOT EXISTS auth_group_permissions_permission_id_idx
                ON auth_group_permissions(permission_id);
            """,
            reverse_sql="""
                DROP INDEX IF EXISTS users_groups_group_id_idx;
                DROP INDEX IF EXISTS users_user_permissions_permission_id_idx;
                DROP INDEX IF EXISTS auth_group_permissions_permission_id_idx;
            """,
        ),
    ]
