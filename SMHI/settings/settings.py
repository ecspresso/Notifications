from pathlib import Path
import configparser

def save(config, file_name):
	if Path(file_name).is_file():
		config.read(file_name)
	try:
		with open(file_name, 'w') as config_file:
			config.write(config_file)
	except Exception as error:
		return error

def load(file_name):
	config = configparser.ConfigParser()
	config.read_file(open(file_name))
	config.read(file_name)
	return config
