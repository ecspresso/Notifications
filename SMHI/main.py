import settings.settings as settings
import pushbullet.notifications as pushbullet
import requests
import uuid
from datetime import datetime

class _Clock:
    def __init__(self, hour, minute):
        self.time = f"{self._add_zero(hour)}:{self._add_zero(minute)}"

    def _add_zero(self, number):
        if number < 10:
            number = f"0{number}"
        return number

class _Weather:
    def __init__(self, code):
        self.forecast = self._translate(code)

    def _translate(self, code):
        return {
        1:  'Clear sky',
        2:  'Nearly clear sky',
        3:  'Variable cloudiness',
        4:  'Halfclear sky',
        5:  'Cloudy sky',
        6:  'Overcast',
        7:  'Fog',
        8:  'Light rain showers',
        9:  'Moderate rain showers',
        10: 'Heavy rain showers',
        11: 'Thunderstorm',
        12: 'Light sleet showers',
        13: 'Moderate sleet showers',
        14: 'Heavy sleet showers',
        15: 'Light snow showers',
        16: 'Moderate snow showers',
        17: 'Heavy snow showers',
        18: 'Light rain',
        19: 'Moderate rain',
        20: 'Heavy rain',
        21: 'Thunder',
        22: 'Light sleet',
        23: 'Moderate sleet',
        24: 'Heavy sleet',
        25: 'Light snowfall',
        26: 'Moderate snowfall',
        27: 'Heavy snowfall'
        }[code]


def weekday_name(day_number):
    return {
        0: 'Monday',
        1: 'Tuseday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }[day_number]


def main():

    try:
        config = settings.load('settings.ini')
    except FileNotFoundError as file_error:
        print('Run setup.py first.')
        raise

    try:
        latitude = config['COORDINATES']['latitude']
        longitude = config['COORDINATES']['longitude']
    except KeyError as key_error:
        if key_error.args[0] in ('COORDINATES','latitude','longitude'):
            print('Run setup.py.')
        raise

    category = 'pmp3g'
    version = 2

    url = f"https://opendata-download-metfcst.smhi.se/api/category/{category}/version/{version}/geotype/point/lon/{longitude}/lat/{latitude}/data.json"
    resp = requests.get(url).json()

    body = []
    # day = weekday_name( datetime.strptime(resp['timeSeries'][1]['validTime'], '%Y-%m-%dT%H:%M:%SZ').weekday())
    day = ''

    for index in range(12):
        date = resp['timeSeries'][index]['validTime']
        parameters = resp['timeSeries'][index]['parameters']
        air_temperature = next((param for param in parameters if param['name'] == 't'), 'No data')
        wind_speed = next((param for param in parameters if param['name'] == 'ws'), 'No data')
        weather = _Weather(next((param for param in parameters if param['name'] == 'Wsymb2'), 'No data')['values'][0])

        if air_temperature['unit'] == 'Cel':
            degree_unit = u'\N{DEGREE SIGN}'
        else:
            degree_unit = air_temperature['unit']

        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        clock = _Clock(date.hour, date.minute)


        if day != weekday_name(date.weekday()):
        	body.append(f"{weekday_name(date.weekday())}:")
        day = weekday_name(date.weekday())

        body.append(f"{clock.time} - {air_temperature['values'][0]}{degree_unit} - {wind_speed['values'][0]}{wind_speed['unit']} - {weather.forecast}")

    body = '\n'.join(body)

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

    data = {
        'iden': uuid.uuid4(),
        'type': 'note',
        'title': 'Todays forecast',
        'body': body
    }
    config['PUSHBULLET']['iden'] = push.create(data)
    settings.save(config, 'settings.ini')

if __name__ == '__main__':
    main()