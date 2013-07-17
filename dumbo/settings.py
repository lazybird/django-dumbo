from django.conf import settings


DUMBO_DATA_DIR = getattr(settings, 'DUMBO_DATA_DIR', '../../sitedata/')

DUMBO_SQL_FILE = 'database.dump'

DUMBO_MEDIA_DUMP_DIR = 'files/'

# A list of keywords that will be checked against the database name.
# Raised a warning if one of these words appear on the database name.
DUMBO_SENSITIVE_KEYWORDS = getattr(settings, 'DUMBO_SENSITIVE_KEYWORDS', ['live'])

DUMBO_RSYNC_OPTIONS = getattr(settings, 'DUMBO_RSYNC_OPTIONS',
    '--recursive --links --times --omit-dir-times '
    '--verbose --delete --exclude=.svn'
)

DUMBO_PG_DUMP_OPTIONS = getattr(settings, 'DUMBO_PG_DUMP_OPTIONS',
    '--no-owner --no-privileges --format=c',
)

# Should not contain the '--dbname' option. It will be added automatically.
DUMBO_PG_RESTORE_OPTIONS = getattr(settings, 'DUMBO_PG_RESTORE_OPTIONS',
    '--no-owner --no-privileges --format=c',
)

DUMBO_CREATE_DB_OPTIONS = getattr(settings, 'DUMBO_CREATE_DB_OPTIONS', '')

DUMBO_ENABLE_SPATIAL = getattr(settings, 'DUMBO_ENABLE_SPATIAL', False)

DUMBO_POSTGIS_TABLES = getattr(settings, 'DUMBO_POSTGIS_TABLES', (
    'spatial_ref_sys',
    'geometry_columns',
    'geography_columns',
))
