#! bin/python

import os
import json
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('map_test.html')

@app.context_processor
def inject_data():
    folder = os.path.dirname(os.path.realpath(__file__))+'/activities'

    gps_points = []

    for subdir, dirs, files in os.walk(folder):
        filenamer = 1
        data = {}
        for filename in files:
            file_path = (subdir+'/'+filename)
            try:
                soup = BeautifulSoup(open(file_path), 'xml')
            except(UnicodeDecodeError):
                print(file_path)
            trps = soup.find_all('trkpt')
            local_points = []
            for point in trps:
                lat = float(point['lat'])
                lon = float(point['lon'])
                local_points.append([lat, lon])
            data["data"+str(filenamer)] = local_points
            filenamer = filenamer + 1
    return dict(gpsdata=data)

#
#
# # filenamer = 1
# #
# # print(len(gps_points))
#
# # for points_set in gps_points:
# #     filename = 'coords/points' + str(filenamer) + '.csv'
# #     f = open(filename, 'w')
# #     for point in points_set:
# #         latlon = '['+ point[0] + ', ' + point[1] + '],\n'
# #         f.write(latlon)
# #     f.close()
# #     filenamer = filenamer + 1

if __name__ == "__main__":
    app.debug = True
    app.run()
