from flask import Flask, render_template
import threading
import serial
import time
import json
import requests
from flask_ngrok import run_with_ngrok

try:
    ports = []
    with open('./comport.txt', 'rt', encoding='UTF8') as f:
        while True:
            msg = f.readline()
            if msg == '#':
                print('end')
                break
            else:
                ports.append(msg[:-1])
    print(ports)
    serialcom = serial.Serial(''+ports[0], timeout=0.1)
    serialcom.bytesize = serial.EIGHTBITS
    serialcom.baudrate = 9600
    serialcom.stopbits = serial.STOPBITS_ONE
    serialcom.parity = serial.PARITY_NONE
    print('arduino connected')
    time.sleep(1)
    with open('./warning.txt', 'rt', encoding='UTF8') as f:
        warning_msg = f.readlines()
    print(warning_msg)
except Exception as e:
    print(e)

test = requests.get('https://fathomless-escarpment-81231.herokuapp.com/api')
test_content = json.loads(test.content)
test_name = []
test_model = []
test_time = []
test_min = []
test_sec = []
test_img = []
currtime = 0
now_test_name = ''
now_test_model = ''
now_test_time = 0
now_test_min = 0
now_test_sec = 0
now_test_img = ''
isStart = 0
for row in test_content:
    test_name.append(str(row['id'])[:-1])
    m, s = map(int, row['time'].split(':'))
    currtime = m*60+s
    test_model.append(str(row['model']))
    test_time.append(currtime)
    test_min.append(m)
    test_sec.append(s)
    test_img.append(row['image'])


def get_arduino():
    global serialcom, test_name, test_time, test_img
    global now_test_time, now_test_model, now_test_name, now_test_img, now_test_min, now_test_sec
    while True:
        #read_msg = serialcom.readline().decode("utf-8").strip()[:11]
        read_msg = serialcom.readline().decode("utf-8").strip()[:-1]
        if read_msg in test_name:
            print('found finally')
            print(read_msg)
            print(test_name.index(read_msg))
            now_test_name = test_name[test_name.index(read_msg)]
            print(now_test_name)
            now_test_time = test_time[test_name.index(read_msg)]
            print(type(now_test_time))
            now_test_img = test_img[test_name.index(read_msg)]
            now_test_model = test_model[test_name.index(read_msg)]
            print(now_test_model)
            now_test_min = test_min[test_name.index(read_msg)]
            now_test_sec = test_sec[test_name.index(read_msg)]
            print(now_test_time)
            print(now_test_min)
            print(now_test_sec)


threading.Thread(target=get_arduino, daemon=True).start()

app = Flask(__name__)
run_with_ngrok(app)


"""@app.route('/api',)
def get_api():
    req = requests.get('http://dnd5eapi.co/api/conditions/blinded')
    print(req.content)
    api_data = json.loads(req)
    return render_template("main.html", api_data=api_data)"""


@app.route('/data', methods=['GET', 'POST'])
def read_data():
    global isStart
    tests = {}
    tests['now_test_name'] = now_test_name
    tests['now_test_time'] = now_test_time
    tests['now_test_img'] = now_test_img
    tests['now_test_model'] = now_test_model
    tests['now_test_min'] = now_test_min
    tests['now_test_sec'] = now_test_sec
    tests['isStart'] = isStart

    return tests


@app.route('/start', methods=['GET', 'POST'])
def set_data():
    global isStart
    isStart = 1
    tests = {}
    return tests


@app.route('/buzzer_on', methods=['GET', 'POST'])
def reset_data():
    global serialcom
    global isStart
    serialcom.write("on".encode())
    isStart = 0
    tests = {}
    return tests


@app.route('/buzzer_off', methods=['GET', 'POST'])
def reset2_data():
    global serialcom
    global isStart
    serialcom.write("off".encode())
    isStart = 0
    tests = {}
    return tests


@app.route('/lcd', methods=['GET', 'POST'])
def reset3_data():
    global serialcom
    global isStart
    serialcom.write("lcd".encode())
    isStart = 0
    tests = {}
    return tests


@app.route('/lcd_off', methods=['GET', 'POST'])
def reset4_data():
    global serialcom
    global isStart
    serialcom.write("lcd_off".encode())
    isStart = 0
    tests = {}
    return tests


@app.route('/', methods=["GET"])
def main():
    req = requests.get('http://dnd5eapi.co/api/conditions/blinded')
    data = req.content
    print(req.content)
    return render_template("main.html", data=data)


@app.route('/main.html')
def gohome():
    return render_template("main.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
