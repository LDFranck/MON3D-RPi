from flask import Flask, render_template, request
from system import System
import sys
import os

sys.path.insert(0, '/mon3d/controller')

app = Flask(__name__)

if not System.has_data_log():
    System.create_data_log()

device_id = System.get_data_log()[1]

@app.get('/')
def get_config():
    return render_template('get_setup.html', device_id=device_id)

@app.post('/')
def post_config():
    wifi_ssid = request.form['ssid']
    wifi_pswd = request.form['pswd']
    os.system(f'WIFI_SSID={wifi_ssid} WIFI_PSWD={wifi_pswd} ./mon3d/boot/mon3d_wifi.sh &')
    return render_template('post_setup.html', device_id=device_id)

if __name__ == '__main__':
    app.run()