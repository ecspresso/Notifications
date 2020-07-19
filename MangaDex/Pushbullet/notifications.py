import requests


class Push:
	def __init__(self, access_token):
		self.access_token = access_token

	def create(self, data, url='https://api.pushbullet.com/v2/pushes'):
		headers = {'Access-Token': self.access_token}
		resp = requests.post(url, headers=headers, data=data)
		iden = resp.json()['iden']
		resp.close()

		return iden

	def delete(self, iden, url='https://api.pushbullet.com/v2/pushes'):
		headers = {'Access-Token': self.access_token}
		requests.delete(f"{url}/{iden}", headers=headers)
