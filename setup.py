try:
	from setuptools import setup
except ImportError:
	raise ImportError(
		"setuptools module required, please go to "
		"https://pypi.python.org/pypi/setuptools and follow the instructions "
		"for installing setuptools"
	)

setup(
	name = 'tt',
	packages = ['tt', 'tt.api'],
	version = '0.1.0',
	description = 'A command line tool for Interval\'s Time Task software',
	license = 'MIT',
	author = 'Ryan Zumstein',
	author_email = 'b57364tc2re@opayq.com',
	url = '',
	scripts = ['tt/tt.py'],
	platforms = 'any',
	keywords = ['python', 'CLI', 'time', 'task', 'time task', 'timetask', 'shell', 'terminal', 'interval', 'intervals'],
	requires = ['dotenv'],
	python_requires = '>=3.6'
)
