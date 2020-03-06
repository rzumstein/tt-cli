import xml.etree.ElementTree as ET

from api.core import make_request

def get_active_project_worktypes(active=True):
	data = make_request('projectworktype/?active=1')
	worktypes = []
	for worktype in data.find('projectworktype').findall('item'):
		worktypes.append({
			'id': worktype.find('id').text,
			'projectid': worktype.find('projectid').text,
			'worktypeid': worktype.find('worktypeid').text,
			'worktype': worktype.find('worktype').text
		})
	print(list(data))
