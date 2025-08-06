from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load data from fixtures'

    def handle(self, *args, **options):
        call_command('flush', interactive=False)
        call_command('loaddata', 'fixtures/category.json')
        call_command('loaddata', 'fixtures/product.json')
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))