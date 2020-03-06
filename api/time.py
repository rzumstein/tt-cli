import xml.etree.ElementTree as ET

from api.core import make_request

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

def add_time(worktypeid, personid, projectid, moduleid, date, hours, billable=1):
	data = make_request('time', 'post', {
		'worktypeid': worktypeid,
		'personid': personid,
		'projectid': projectid,
		'moduleid': moduleid,
		'date': date,
		'time': hours,
		'billable': 1 if billable else 0
	})
	return data
