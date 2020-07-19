import settings.settings as settings
import configparser

def setup():
	rss = input('Enter RSS url: ')
	access_token = input('Enter Pushbullet access token: ')

	values = {
		'RSS': {
			'url': rss
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