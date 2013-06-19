from optparse import make_option
import commands
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from dumbo import settings as dumbo_settings
from dumbo.utils import get_logger


logger = get_logger('dumbo')


class DumboCommand(object):
    option_list = BaseCommand.option_list + (
        make_option('--path',
            action='store',
            dest='dump_dir',
            type='string',
            help='Path to the data folder',
        ),
    )

    @property
    def database_params(self):
        return {
            'host': settings.DATABASES['default']['HOST'],
            'user': settings.DATABASES['default']['USER'],
            'name': settings.DATABASES['default']['NAME'],
            'sql_file': self.sql_file,
        }

    @property
    def media_params(self):
        return {
            'media_dump_dir': self.media_dump_dir,
            'media_dir': self.media_dir,
        }

    def set_dump_dir(self, options):
        """
        Sets the dump folder path and verify that it exists.
        """
        self.dump_dir = options.get('dump_dir') or dumbo_settings.DUMBO_DATA_DIR
        self.sql_file = os.path.join(self.dump_dir, dumbo_settings.DUMBO_SQL_FILE)
        if not os.path.exists(self.dump_dir):
            raise CommandError(
                'Folder does not exist: {}\n'.format(self.dump_dir)
            )
        logger.info('Using folder "{}"'.format(self.dump_dir))
        return self.dump_dir

    def set_media_dir(self):
        """
        Sets path to media folders. Verifies that the project
        media folder exists.
        """
        self.media_dump_dir = os.path.join(
            self.dump_dir,
            dumbo_settings.DUMBO_MEDIA_DUMP_DIR
        )
        self.media_dir = settings.MEDIA_ROOT
        if not os.path.exists(self.media_dir):
            raise CommandError(
                'Media folder does not exist: {}\n'.format(self.media_dir)
            )
        if not os.path.exists(self.media_dump_dir):
            logger.warning('Creating folder "{}".'.format(self.media_dump_dir))
            os.mkdir(self.media_dump_dir)

    def run_shell_command(self, cmd, fail_fast=True):
        """
        Run a shell command.
        """
        status, output = commands.getstatusoutput(cmd)
        if status != 0 and fail_fast:
            logger.error(output)
            raise CommandError(output)
        logger.info('Executed: {}'.format(cmd))
        if output:
            if status != 0:
                # There was an error but we did not fail-fast.
                logger.warning(output)
            else:
                logger.info(output)
        return status

    def run_sql_command(self, sql, db_name=None):
        """
        Runs an SQL command as superuser.
        """
        db_name = db_name or self.database_params['name']
        # Wraps the given SQL statement so that it can be piped into psql.
        # Escapes for the echo statement to handle quotes.
        command = (
            """sudo su postgres -c "echo \\\"{sql}\\\" | """
            """psql {db_name}" """.format(sql=sql, db_name=db_name)
        )
        self.run_shell_command(command)
