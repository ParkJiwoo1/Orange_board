import datetime
from flask import Flask, render_template
from datetime import datetime
import threading
import serial
import time
import json
import requests
from openpyxl import load_workbook
load_wb = load_workbook("data.xlsx", data_only=True)
# 시트 이름으로 불러오기
load_ws = load_wb['Sheet1']

"""data_name=[]
data_time=[]
data_des=[]
for row in load_ws.rows:
    data_name.append(str(row[0].value[1:]))
    data_time.append(row[1].value)
    data_des.append(row[2].value)
print(data_name)
print(data_time)
print(data_des)
now_data_name='' 
now_data_time=0
now_data_des=''    
is_start=0   """

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

    test = requests.get(
        'https://fathomless-escarpment-81231.herokuapp.com/api')
test_content = json.loads(test.content)
test_name = []
test_time = []
test_img = []
currtime = 0
now_test_name = ''
now_test_time = 0
now_test_img = ''
isStart = 0
for row in test_content:
    # print(row)
    test_name.append(str(row['id'])[:-1])
    m, s = map(int, row['time'].split(':'))
    currtime = m*60+s
    test_time.append(currtime)
    test_img.append(row['image'])
print(test_name)
print(test_time)
print(test_img)


def get_arduino():
    global serialcom, data_name, data_time, data_des
    global now_data_name, now_data_time, now_data_des
    while True:
        read_msg = serialcom.readline().decode("utf-8").strip()
        # read_msg=serialcom.readline().decode("utf-8")[:-2]
        # print(read_msg)
        if read_msg in data_name:
            print('found finally')
            print(read_msg)
            print(test_name.index(read_msg))
            now_test_name = test_name[test_name.index(read_msg)]
            print(now_test_name)
            now_test_time = test_time[test_name.index(read_msg)]
            print(type(now_test_time))
            now_test_img = test_img[test_name.index(read_msg)]


threading.Thread(target=get_arduino, daemon=True).start()

app = Flask(__name__)


@app.route('/api',)
def get_api():
    req = requests.get('http://dnd5eapi.co/api/conditions/blinded')
    print(req.content)
    api_data = json.loads(req)
    return render_template("main.html", api_data=api_data)


@app.route('/data', methods=['GET', 'POST'])
def read_data():
    global is_start
    tests = {}
    num = 1
    tests['now_test_name'] = now_test_name
    tests['now_test_time'] = now_test_time
    tests['now_test_img'] = now_test_img
    tests['isStart'] = isStart

    return tests


@app.route('/start', methods=['GET', 'POST'])
def set_data():
    global is_start
    isStart = 1
    tests = {}
    return tests


@app.route('/buzzer_on', methods=['GET', 'POST'])
def reset_data():
    global is_start, serialcom
    serialcom.write("on".encode())
    isStart = 0
    tests = {}
    return tests


@app.route('/buzzer_off', methods=['GET', 'POST'])
def reset2_data():
    global is_start, serialcom
    serialcom.write("off".encode())
    is_start = 0
    datas = {}
    return datas


@app.route('/', methods=["GET"])
def hello():
    req = requests.get('http://dnd5eapi.co/api/conditions/blinded')
    data = req.content
    print(req.content)

    return render_template("main.html")


@app.route('/main.html')
def gohome():
    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug=True)
