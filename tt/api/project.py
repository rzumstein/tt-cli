from api.core import make_request

def get_projects(active=1):
	data = make_request('project/?active={0}'.format(active))
	projects = []
	for project in data.find('project').findall('item'):
		projects.append({
			'id': project.find('id').text,
			'name': project.find('name').text
		})
	return projects
