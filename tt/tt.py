#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import sys
import termgraph

from collections import defaultdict
from dotenv import load_dotenv
from math import floor

from api.projectmodule import get_project_modules
from api.project import get_projects
from api.projectworktype import get_project_worktypes
from api.time import add_time, get_time

load_dotenv()

logging.basicConfig(filename='../tt.log', filemode='w+', level=int(os.getenv('LOG_LEVEL')))

def log_exception(type, value, tb):
	logging.exception('Uncaught exception: {0}'.format(str(value)))
	print(str(e))

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

command = None
try:
	if args.get:
		command = 'get'
	elif args.add:
		command = 'add'
except AttributeError as e:
	print(str(e))
	time_parser.print_help()

if command == 'get':
	time_entries = defaultdict(list)
	for time_entry in get_time():
		time_entries[time_entry['date']].append(time_entry['time'])
	for date, times in time_entries.items():
		time = sum(list(map(float, times)))
		print('{0}: {1} {2}'.format(date, '▇' * floor(time), time))
elif command == 'add':
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
