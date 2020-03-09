#!/usr/bin/env python3

import argparse
import logging
import os

from dotenv import load_dotenv

from api.projectmodule import get_project_modules
from api.project import get_projects
from api.projectworktype import get_project_worktypes
from api.time import add_time, get_time

load_dotenv()

logging.basicConfig(filename='tt.log', filemode='w+', level=int(os.getenv('LOG_LEVEL')))

def log_exception(type, value, tb):
    logging.exception('Uncaught exception: {0}'.format(str(value)))
    print(str(value))

def display_options_to_user(title, opts):
	print('\n{0}\n{1}'.format(title, '-' * len(title)))
	for opt in opts:
		print('{0}\t {1}'.format(opt['id'], opt['name']))
	print()

def extract_ids(obj):
	return [o['id'] for o in obj]

def prompt_user_for_id(prompt_text, ids):
	s = input(prompt_text)
	while not any(i == s for i in ids):
		s = input(prompt_text)
	return s

def get_id_from_user(id_type, data):
	display_options_to_user(id_type + 's', data)
	return prompt_user_for_id('Please select a {0} ID: '.format(id_type), extract_ids(data))

def get_project_id_from_user():
	return get_id_from_user('Project', get_projects())

def get_project_module_id_from_user(project_id):
	return get_id_from_user('Module', get_project_modules(project_id))

def get_project_worktype_id_from_user(project_id):
	return get_id_from_user('Worktype', get_project_worktypes(project_id))

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

try:
	if args.get:
		time_entries = get_time()
		for time_entry in time_entries:
			print('Date: {0}'.format(time_entry['date']))
			print('Time: {0}h'.format(time_entry['time']))
			print('Description: {0}'.format(time_entry['description']))
			print('----\n')

	if args.add:
		project_id = get_project_id_from_user()
		module_id = get_project_module_id_from_user(project_id)
		worktype_id = get_project_worktype_id_from_user(project_id)
		date = args.date if args.date else input('\nDate (yyyy-mm-dd): ')
		time = args.time if args.time else input('\nTime (h): ')
		print()
		description = input('Description: ')
		while len(description) > 255:
			print('\nDescription must be 255 characters or fewer.\n')
			description = input('Description: ')
		print()
		if add_time(project_id, module_id, worktype_id, date, time, args.billable, description):
			print('Added {0} hours of time on {1}'.format(time, date))
		else:
			print('Failed adding time. See log for more details')
except AttributeError:
	time_parser.print_help()
