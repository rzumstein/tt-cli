from api.core import make_request

def get_project_modules(project_id, active=1):
	data = make_request(
		'projectmodule/?projectid={0}&active={1}'
		.format(project_id, active)
	)
	modules = []
	for module in data.find('projectmodule').findall('item'):
		modules.append({
			'id': module.find('moduleid').text,
			'name': module.find('modulename').text
		})
	return modules
