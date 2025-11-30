import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hishamAiAgentOS.settings')
django.setup()

from apps.users.models import HishamOSUser

username = 'admin'
email = 'admin@hishamos.local'
password = 'Amman123'

if HishamOSUser.objects.filter(username=username).exists():
    print(f'User "{username}" already exists')
    user = HishamOSUser.objects.get(username=username)
else:
    user = HishamOSUser.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Admin',
        last_name='User',
        role='ADMIN'
    )
    print(f'Superuser "{username}" created successfully!')

print(f'\nUsername: {user.username}')
print(f'Email: {user.email}')
print(f'Is superuser: {user.is_superuser}')
print(f'Is staff: {user.is_staff}')
print(f'Role: {user.role}')
