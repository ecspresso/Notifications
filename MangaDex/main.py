import rss.parser as rss
import pushbullet.notifications as pushbullet
import settings.settings as settings
import uuid

def get_new_chapters(last_seen, rss_url):
	feed = rss.Parser(rss_url).get_feed()
	new_chapters = []

	for chapter in feed['entries']:
		if last_seen != chapter['id']:
			new_chapters.append(chapter)
		else:
			return new_chapters

def get_newest_chapter(rss_url):
	feed = rss.Parser(rss_url).get_feed()
	new_chapters = []
	new_chapters.append(feed['entries'][0])
	return new_chapters



def main():
	# Import config to load configurations
	try:
		config = settings.load('settings.ini')
	except FileNotFoundError as file_error:
		print('Run setup.py first.')
		raise


	# Placeholder for new chapters
	try:
		new_chapters = get_new_chapters(config['MANGA']['latest'], config['RSS']['url'])
	except KeyError as key_error:
		if key_error.args[0] in ('MANGA','latest'):
			new_chapters = get_newest_chapter(config['RSS']['url'])
		else:
			raise



	if new_chapters:
		try:
			push = pushbullet.Push(config['PUSHBULLET']['access_token'])
			push.delete(config['PUSHBULLET']['iden'])
		except KeyError as key_error:
			if key_error.args[0] == 'iden':
				pass
			elif key_error.args[0] == 'PUSHBULLET':
				print('Pusbullet section is missing. Run setup.py.')
				raise
			elif key_error.args[0] == 'access_token':
				print('Pushbullet access token is missing. Run setup.py.')
				raise
			else:
				raise

		config['MANGA']['latest'] = new_chapters[0]['id']
		config['MANGA']['title'] = new_chapters[0]['title']

		body = []
		for index in range(len(new_chapters)):
			body.append(new_chapters[index - 1]['title'] + '\n')

		body.sort()
		body = ''.join(body)

		data = {
			'iden': uuid.uuid4(),
			'type': 'note',
			'title': 'New chapters to read!',
			'body': body
		}
		config['PUSHBULLET']['iden'] = push.create(data)

		settings.save(config, 'settings.ini')

if __name__ == '__main__':
	main()