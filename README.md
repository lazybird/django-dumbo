Django Dumbo
============

django-dumbo provides management commands for dumping and loading your
project database and media files. It comes with spatial database support.
It works with postgreSQL.

Usage Example
-------------

### Dump Data

The dump command creates a `site_data` folder with an SQL dump
and backup of your project media files.

*The folder must be created prior to dumping data*


    mkdir ../../sitedata/
    ./manage.py dumbo_dump_data --path=../../sitedata/


### Load Data

The load command finds the database dump in the given folder. It loads
the SQL dump and restores your project media files.

    ./manage.py dumbo_load_data --path=../../sitedata/


### Default data folder

If no path is provided, the commands will use a default folder
to backup and restore data. The default folder is configurable
in settings.

    ./manage.py dumbo_dumpdata
    ./manage.py dumbo_load_data


Installation
------------

Install the package using something like pip and add `dumbo` to
your `INSTALLED_APPS` setting.


Settings
--------

### Data folder

The folder to use when backing-up and restoring data:

    DUMBO_DATA_DIR = '../../sitedata/'


### Rsync options

You can customize the `rsync` options with this setting:

    DUMBO_RSYNC_OPTIONS = '--recursive --links --times --omit-dir-times --verbose --delete --exclude=.svn'


### PostgreSQL command options

You can customize the `pg_dump` `pg_restore` options with these setting:

    DUMBO_PG_DUMP_OPTIONS = '--no-owner --no-privileges --format=c',

    DUMBO_PG_RESTORE_OPTIONS = '--format=c',


For instance, here is how you could exclude the Django session table.
You will have to run `syncdb` to recreate it after loading the data.

    DUMBO_PG_DUMP_OPTIONS = '--no-owner --no-privileges --exclude-table=django_session --format=c'


You can also customize the options for the `createdb` command.

    DUMBO_CREATE_DB_OPTIONS = ''


### Spatial database

If spatial database is enabled, the PostGIS extension will be created.

    DUMBO_ENABLE_SPATIAL = False

In addition to creating PostGIS extension, some tables permissions
will be altered. You can configure the list of tales:

    DUMBO_POSTGIS_TABLES = ('spatial_ref_sys', 'geometry_columns', 'geography_columns')

### Sensitive keywords in database name

You can raise a warning message and prompt the user for authorisation when
a given keywords is found in the database name.

    DUMBO_SENSITIVE_KEYWORDS = ['staging', 'live']
