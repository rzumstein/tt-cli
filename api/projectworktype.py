from api.core import make_request

def get_project_worktypes(project_id, active=1):
	data = make_request(
		'projectworktype/?projectid={0}&active={1}'
		.format(project_id, active)
	)
	worktypes = []
	for worktype in data.find('projectworktype').findall('item'):
		worktypes.append({
			'id': worktype.find('worktypeid').text,
			'name': worktype.find('worktype').text
		})
	return worktypes
