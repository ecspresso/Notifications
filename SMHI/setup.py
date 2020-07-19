import settings.settings as settings
import configparser

def setup():
	longitude = input('Enter longitude: ')
	latitude = input('Enter latitude: ')
	access_token = input('Enter Pushbullet access token: ')

	values = {
		'COORDINATES': {
			'longitude': longitude,
			'latitude': latitude
		},
		'PUSHBULLET': {
			'access_token': access_token
		}
	}

	config = configparser.ConfigParser()
	for v in values:
		config[v] = values[v]

	settings.save(config, 'settings.ini')

if __name__ == '__main__':
	setup()