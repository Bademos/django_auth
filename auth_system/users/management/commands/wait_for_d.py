# users/management/commands/wait_for_db.py
import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database to be available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        max_retries = 30
        retries = 0

        while not db_conn and retries < max_retries:
            try:
                db_conn = connections['default'].cursor()
            except OperationalError:
                self.stdout.write(f'Database unavailable, waiting 1 second... (attempt {retries + 1}/{max_retries})')
                time.sleep(1)
                retries += 1

        if db_conn:
            self.stdout.write(self.style.SUCCESS('Database available!'))
        else:
            self.stdout.write(self.style.ERROR('Database unavailable!'))
            raise Exception('Database connection failed')