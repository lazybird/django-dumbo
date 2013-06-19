import os

from django.core.management.base import BaseCommand

from dumbo import settings as dumbo_settings
from dumbo.management.commands.base import DumboCommand


class Command(DumboCommand, BaseCommand):
    help = 'Loads the database dump and the media files.'

    def handle(self, **options):
        self.set_dump_dir(options)
        self.reset_database()
        self.enable_spatial_database()
        self.load_data()
        self.set_media_dir()
        self.copy_media_files()

    def reset_database(self):
        params = self.database_params.copy()
        dropdb_cmd = 'sudo su postgres -c "dropdb {name}"'.format(**params)
        self.run_shell_command(dropdb_cmd, fail_fast=False)
        params['options'] = dumbo_settings.DUMBO_CREATE_DB_OPTIONS
        createdb_cmd = (
            'sudo su postgres -c "createdb {options} '
            '--owner={user} {name}"'.format(**params)
        )
        self.run_shell_command(createdb_cmd)

    def enable_spatial_database(self):
        if not dumbo_settings.DUMBO_ENABLE_SPATIAL:
            return None
        self.run_sql_command('CREATE EXTENSION postgis;')
        params = self.database_params.copy()
        for table_name in dumbo_settings.DUMBO_POSTGIS_TABLES:
            params['table'] = table_name
            sql = 'ALTER TABLE {table} OWNER TO {user};'.format(**params)
            self.run_sql_command(sql)

    def load_data(self):
        params = self.database_params.copy()
        params['options'] = dumbo_settings.DUMBO_PG_RESTORE_OPTIONS
        pg_restore_cmd = (
            'pg_restore -h {host} -U {user} {options} '
            '--dbname={name} {sql_file}'.format(**params)
        )
        self.run_shell_command(pg_restore_cmd, fail_fast=False)

    def copy_media_files(self):
        params = self.media_params.copy()
        params['options'] = dumbo_settings.DUMBO_RSYNC_OPTIONS
        rsync_cmd = (
            'rsync {options} {media_dump_dir} {media_dir}'.format(**params)
        )
        self.run_shell_command(rsync_cmd)
