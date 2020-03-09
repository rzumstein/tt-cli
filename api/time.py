import xml.etree.ElementTree as ET

from api.core import get_personid, make_request

def get_time():
	data = make_request('time')
	time_entries = []
	for entry in data.find('time').findall('item'):
		time_entries.append({
			'date': entry.find('date').text,
			'time': entry.find('time').text,
			'description': entry.find('description').text
		})
	return time_entries

def add_time(projectid, moduleid, worktypeid, date, hours, billable=1, description=''):
	data = make_request('time', 'post', {
		'projectid': projectid,
		'moduleid': moduleid,
		'worktypeid': worktypeid,
		'personid': get_personid(),
		'date': date,
		'time': hours,
		'billable': 1 if billable else 0,
		'description': description
	})
	return data
