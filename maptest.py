import os
import json
import six
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import redis

app = Flask(__name__)

@app.route('/runmap', methods=['GET', 'POST'])
def index():
    return render_template('map_test.html')

@app.context_processor
def inject_data():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    folder = os.path.dirname(os.path.realpath(__file__))+'/activities'

    gps_points = []
    if r.get('data'):
        data = json.loads(r.get('data'))
        return dict(gpsdata = data)
    else:
        for subdir, dirs, files in os.walk(folder):
            filenamer = 1
            data = {}

            for filename in files:
                file_path = (subdir+'/'+filename)
                try:
                    soup = BeautifulSoup(open(file_path), 'xml')
                except(UnicodeDecodeError):
                    six.print_(file_path)
                trps = soup.find_all('trkpt')
                local_points = []
                for point in trps:
                    lat = float(point['lat'])
                    lon = float(point['lon'])
                    local_points.append([lat, lon])
                data["data"+str(filenamer)] = local_points
                data_json = json.dumps(data)
                r.set('data', data_json)
                print r.get('data')
                filenamer = filenamer + 1
        return dict(gpsdata=data)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
