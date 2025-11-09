from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post, Comment

class Command(BaseCommand):
    help = 'Setup user groups and permissions'

    def handle(self, *args, **options):
        # Create Authors group
        authors_group, created = Group.objects.get_or_create(name='Authors')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Authors group'))
        
        # Create Readers group
        readers_group, created = Group.objects.get_or_create(name='Readers')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Readers group'))

        # Add permissions to Authors group
        post_content_type = ContentType.objects.get_for_model(Post)
        comment_content_type = ContentType.objects.get_for_model(Comment)
        
        # Get all permissions for Post model
        post_permissions = Permission.objects.filter(content_type=post_content_type)
        authors_group.permissions.add(*post_permissions)
        
        # Add comment permissions to Authors
        comment_permissions = Permission.objects.filter(
            content_type=comment_content_type,
            codename__in=['add_comment', 'change_comment', 'delete_comment', 'view_comment']
        )
        authors_group.permissions.add(*comment_permissions)
        
        # Add basic permissions to Readers group
        readers_group.permissions.add(
            Permission.objects.get(codename='view_post', content_type=post_content_type),
            Permission.objects.get(codename='add_comment', content_type=comment_content_type),
            Permission.objects.get(codename='view_comment', content_type=comment_content_type),
        )

        self.stdout.write(self.style.SUCCESS('Successfully setup groups and permissions'))