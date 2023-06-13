from django.core.management.base import BaseCommand

from ._convert_to_models import convert_to_models


class Command(BaseCommand):
    help = 'Uploading work to database'

    def handle(self, *args, **options):
        result = convert_to_models()
        if 'error' in result:
            message = ''
            for item in result:
                message += (
                    f'Error loading! {item}\n' if item != 'error' else ''
                )
            return self.stdout.write(self.style.WARNING(message))
        return self.stdout.write(
            self.style.SUCCESS('The data is loaded!')
        )
