"""
Django management command to wait for the database to be ready.
"""
import time

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Wait for database to be ready."""
    def handle(self, *args, **kwargs):
        self.stdout.write('Waiting for database...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                self.stdout.flush()
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))

          