from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Create moderator groups with permissions'

    def handle(self, *args, **options):
        product_content_type = ContentType.objects.get_for_model(Product)
        
        unpublish_permission = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=product_content_type
        )
        
        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=product_content_type
        )
        
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        moderator_group.permissions.add(unpublish_permission, delete_permission)
        
        self.stdout.write(
            self.style.SUCCESS('Группы созданы успешно')
        )