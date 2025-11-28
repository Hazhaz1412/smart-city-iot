from django.core.management.base import BaseCommand
from django.db.models import Count
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Fix duplicate Google OAuth users'

    def handle(self, *args, **options):
        self.stdout.write('Checking for duplicate users...\n')
        
        # Find users with duplicate emails
        duplicates = CustomUser.objects.values('email').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        if not duplicates:
            self.stdout.write(self.style.SUCCESS('✓ No duplicate users found'))
            return
        
        for dup in duplicates:
            email = dup['email']
            self.stdout.write(f'\n📧 Email: {email} ({dup["count"]} users)')
            
            users = CustomUser.objects.filter(email=email).order_by('date_joined')
            
            # Keep the oldest user (first registered)
            keep_user = users.first()
            delete_users = users.exclude(id=keep_user.id)
            
            self.stdout.write(f'  ✓ Keeping: ID={keep_user.id}, Username={keep_user.username}')
            
            for user in delete_users:
                self.stdout.write(f'  ✗ Deleting: ID={user.id}, Username={user.username}')
                # Transfer devices if any
                from accounts.models import UserDevice
                device_count = UserDevice.objects.filter(user=user).count()
                if device_count > 0:
                    self.stdout.write(f'    → Transferring {device_count} devices to {keep_user.username}')
                    UserDevice.objects.filter(user=user).update(user=keep_user)
                
                # Delete user
                user.delete()
                self.stdout.write(self.style.SUCCESS(f'    ✓ Deleted user {user.username}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Cleanup complete!'))
