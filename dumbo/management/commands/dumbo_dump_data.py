from django.core.management.base import BaseCommand

from dumbo import settings as dumbo_settings

from dumbo.management.commands.base import DumboCommand


class Command(DumboCommand, BaseCommand):
    help = 'Dumps the database and the media files.'

    def handle(self, **options):
        self.set_dump_dir(options)
        self.dump_data()
        self.set_media_dir()
        self.copy_media_files()

    def dump_data(self):
        params = self.database_params.copy()
        params['options'] = dumbo_settings.DUMBO_PG_DUMP_OPTIONS
        pg_dump_cmd = (
            'pg_dump -h {host} -U {user} {options} {name} > '
            '{sql_file}'.format(**params)
        )
        self.run_shell_command(pg_dump_cmd)

    def copy_media_files(self):
        params = self.media_params.copy()
        params['options'] = dumbo_settings.DUMBO_RSYNC_OPTIONS
        rsync_cmd = 'rsync {options} {media_dir} {media_dump_dir}'.format(**params)
        self.run_shell_command(rsync_cmd)
