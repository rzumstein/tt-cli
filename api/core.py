import logging
import os
import requests
import xml.etree.ElementTree as ET

personid = None

def get_auth():
	return (os.getenv('API_USER_TOKEN'), os.getenv('API_ARBITRARY_PASSWORD'))

def get_personid():
	global personid
	if not personid:
		data = make_request('person/?username={0}'.format(os.getenv('TIME_TASK_USERNAME')))
		personid = data.find('person').find('item').find('id').text
	return personid

def make_request(endpoint, method='get', body={}):
	r = requests.request(
		method,
		'https://api.myintervals.com/' + endpoint,
		auth=get_auth(),
		headers={'Accept': 'application/xml'},
		json=body
	)
	t = ET.fromstring(r.text)
	if r.status_code > 399:
		logging.critical('Failed making request to TimeTask API')
		logging.critical(r.text)
		exit(
			'Critical error when making request to TimeTask API:\n{message}\n{verbose}'
			.format(
				message=t.find('error').find('message').text,
				verbose='\n'.join([err.text for err in list(t.find('error').find('verbose'))])
			)
		)
	return t
