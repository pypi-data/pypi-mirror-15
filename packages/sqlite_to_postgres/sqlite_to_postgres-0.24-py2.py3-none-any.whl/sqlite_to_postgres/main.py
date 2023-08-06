#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import time

from cdis_pipe_utils import df_util
from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util


def write_pgpass(conn_dict,logger):
    pgpass_string = conn_dict['hostname'] + ':' + conn_dict['port'] + ':' + conn_dict['database'] + ':' + conn_dict['username'] + \
                     ':' + conn_dict['password']
    home_dir = os.path.expanduser('~')
    pgpass_path = os.path.join(home_dir, '.pgpass')
    if os.path.exists(pgpass_path):
        os.remove(pgpass_path)
    with open(pgpass_path, 'w') as f_open:
        f_open.write(pgpass_string)
    os.chmod(pgpass_path, 0o400)
    return pgpass_path

def allow_create_fail(sql_path, logger):
    shell_cmd = "sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' " + sql_path + " > create_table.sql"
    pipe_util.do_shell_command(shell_cmd, logger)
    shell_cmd = "sed 's/CREATE INDEX/CREATE INDEX IF NOT EXISTS/g' create_table.sql > " + sql_path
    pipe_util.do_shell_command(shell_cmd, logger)
    return

def main():
    parser = argparse.ArgumentParser('write sqlite file to postgres')
    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)

    parser.add_argument('--source_sqlite_path', required=True)
    parser.add_argument('--postgres_cred_path', required=False)
    parser.add_argument('--postgres_creds_s3url', required=False)
    parser.add_argument('--s3cfg_path', required=False)
    parser.add_argument('--ini_section', required=True)
    parser.add_argument('--uuid', required=True)
    args = parser.parse_args()

    
    source_sqlite_path = args.source_sqlite_path
    ini_section = args.ini_section
    uuid = args.uuid
    
    tool_name = 'sqlite_to_postgres'
    logger = pipe_util.setup_logging(tool_name, args, uuid)

    step_dir = os.getcwd()
    if pipe_util.already_step(step_dir, uuid + '_stop', logger):
        logger.info('already completed step `sqlite_to_postgres`')
    else:
        logger.info('running step `sqlite_to_postgres`')


        
        source_sqlite_name, source_sqlite_ext = os.path.splitext(os.path.basename(source_sqlite_path))
        logger.info('source_sqlite_name = %s' % source_sqlite_name)

        #dump
        source_dump_name = source_sqlite_name + '.sql'
        cmd = ['sqlite3', source_sqlite_path, "\'.dump\'", '>', source_dump_name ]
        shell_cmd = ' '.join(cmd)
        pipe_util.do_shell_command(shell_cmd, logger)


        #alter text create table/index
        allow_create_fail(source_dump_name, logger)

        #get postgres creds
        try:
            postgres_creds_path = args.postgres_creds_path
            kwargs = {'db_cred_path': postgres_creds_path,
                       'ini_section': ini_section, 'logger': logger}
            conn_dict = pipe_util.get_connect_dict(**kwargs)
        except NameError:
            postgres_creds_s3url = args.postgres_creds_s3url
            s3cfg_path = args.s3cfg_path
            kwargs = {'db_cred_s3url': postgres_creds_s3url, 's3cfg_path': s3cfg_path,
                      'ini_section': ini_section, 'logger': logger}
            conn_dict = pipe_util.get_connect_dict(**kwargs)
        pgpass_path = write_pgpass(conn_dict,logger)

        #load
        cmd = ['psql', '-f', source_dump_name, '-U', conn_dict['username'], '-w', '-d', conn_dict['database'], '-h', conn_dict['hostname']]
        logger.info('cmd=%s' % cmd)
        env = dict()
        env.update(os.environ)
        env['PGPASSFILE'] = pgpass_path
        output = subprocess.check_output(cmd, env=env, stderr=subprocess.STDOUT)
        os.remove(pgpass_path)
        logger.info('b output=\n%s' % output.decode().format())
        logger.info('\noutput=\n%s' % output)

        pipe_util.create_already_step(step_dir, uuid + '_stop', logger)
    return

if __name__ == '__main__':
    main()
