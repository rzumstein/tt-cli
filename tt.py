#!/usr/bin/env python3

import argparse
import logging
import os

from dotenv import load_dotenv

from api.projectworktype import get_active_project_worktypes
from api.time import add_time, get_time

load_dotenv()

logging.basicConfig(filename='tt.log', filemode='w+', level=int(os.getenv('LOG_LEVEL')))

def log_exception(type, value, tb):
    logging.exception('Uncaught exception: {0}'.format(str(value)))
    print(str(value))

parent_parser = argparse.ArgumentParser(add_help=False)
main_parser = argparse.ArgumentParser(description='TimeTask CLI')

time_subparsers = main_parser.add_subparsers(title='time subcommands', description='valid time subcommands')
time_parser = time_subparsers.add_parser('time')
time_group = time_parser.add_mutually_exclusive_group()
time_group.add_argument('-g', '--get', nargs='?', const=True, help='get time entries')
time_group.add_argument('-a', '--add', nargs='?', const=True, help='add time entry')
time_parser.add_argument('-d', '--date', nargs='?', help='date')
time_parser.add_argument('-t', '--time', nargs='?', help='time (hours)')
time_parser.add_argument('-b', '--billable', action='store_true', help='billable')

args = main_parser.parse_args()
print('args: {0}'.format(args))

if args.get:
	time_entries = get_time()
	for time_entry in time_entries:
		print('Date: {0}'.format(time_entry['date']))
		print('Time: {0}h'.format(time_entry['time']))
		print('Description: {0}'.format(time_entry['description']))
		print('----\n')

if args.add:
	get_active_project_worktypes()
	exit()
	if not args.date:
		time_parser.error('--add requires --date')
	if not args.time:
		time_parser.error('--add requires --time')
	worktypeid = input('worktypeid: ')
	personid = input('personid: ')
	projectid = input('projectid: ')
	moduleid = input('moduleid: ')
	if add_time(worktypeid, personid, projectid, moduleid, args.date, args.time, args.billable):
		print('Added {0} hours of time on {1}'.format(args.time, args.date))
	else:
		print('Failed adding time. See log for more details')
