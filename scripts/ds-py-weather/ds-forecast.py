import json
import urllib.request
from datetime import datetime

def bearing_to_compass(b):
    # List of possible compass directions and their bearing in degrees.
    direction = {
        'N': 0,
        'NE': 45,
        'E': 90,
        'SE': 135,
        'S': 180,
        'SW': 225,
        'W': 270,
        'NW': 315
    }

    # Because Bearing can be anything from 0 to 359, we need to cycle through them. Let's start with North.

    cur_dir = 'N' #<- Keep track of which compass direction we're on.
    for k in direction:

        # If the bearing value is greater than the direction we're currently on, update the value.
        if b > direction[k]:
            cur_dir = k

    # Return the value.
    return cur_dir

# Download a webpage the easy way
def download_url(url):
    output = ""
    with urllib.request.urlopen(url, data=None) as response:
        output = response.read()

    return output


key = "your-key-here"
#lat = "41.1590783" <- Change this
#lon = "-75.1271883" <- Change this

uri = "https://api.darksky.net/forecast/{}/{},{}".format(key, lat, lon)
ds_json = download_url(uri)
ds_dict = json.loads(ds_json)

# Report hash
report = {}

report_date_raw = ds_dict['currently']['time']
#DateTime.strftime("1318996912", '%s')
report['date'] = datetime.utcfromtimestamp(report_date_raw).strftime("%I:%M%P on %A, %B %d, %Y")

rain = ds_dict['daily']['data'][0]['precipProbability'] * 100
report['rain_chance'] = "Rain chance: {}".format(rain)

report['condition'] = "Summary: {}".format(ds_dict['currently']['summary'])

cur_temp = ds_dict['currently']['temperature']
report['temp_cur'] = "Current temperature: {} F".format(cur_temp)

cur_hi = ds_dict['daily']['data'][0]['temperatureHigh']
report['temp_hi'] = "High today: {}F".format(cur_hi)

cur_lo = ds_dict['daily']['data'][0]['temperatureLow']
report['temp_lo'] = "Low today: {}F".format(cur_lo)

cur_ws = ds_dict['currently']['windSpeed']
report['wind_speed'] = "Wind speed: {}mph".format(cur_ws)

wd = bearing_to_compass(ds_dict['currently']['windBearing'])
report['wind_direction'] = "Wind direction: {}".format(wd)

# Add whatever information you want in your weather report using the examples
# above.

for k in report:
	print(report[k])
