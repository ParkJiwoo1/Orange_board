from flask import Flask, render_template
import threading
import serial
import time
import json
import requests
from openpyxl import load_workbook
load_wb = load_workbook("data.xlsx", data_only=True)
# 시트 이름으로 불러오기 
load_ws = load_wb['Sheet1']

data_name=[]
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
is_start=0   

try:
    ports=[]
    with open('./comport.txt','rt',encoding='UTF8') as f:
        while True:
            msg=f.readline()
            if msg=='#':
                print('end')
                break
            else:
                ports.append(msg[:-1])
    print(ports)
    serialcom=serial.Serial('COM'+ports[0],timeout=0.1)
    serialcom.bytesize=serial.EIGHTBITS
    serialcom.baudrate=9600
    serialcom.stopbits=serial.STOPBITS_ONE
    serialcom.parity=serial.PARITY_NONE
    print('arduino connected')
    time.sleep(1)
    with open('./warning.txt','rt',encoding='UTF8') as f:
        warning_msg=f.readlines()
    print(warning_msg)
except Exception as e:
    print(e)
    
test = requests.get('https://fathomless-escarpment-81231.herokuapp.com/api')
test_content = json.loads(test.content)
def get_arduino():
    global serialcom,data_name,data_time,data_des
    global now_data_name,now_data_time,now_data_des
    while True:
         read_msg=serialcom.readline().decode("utf-8").strip()
         #read_msg=read_msg.decode('utf-8',errors='strict')
         #read_msg=read_msg[:-2]
         #print(read_msg)
         #if(read_msg==test_content[0]['id']):
         #print(read_msg)
           #print('found it')
         if read_msg in data_name:
             print('find index')
             print(data_name.index(read_msg))
             now_data_name=data_name[data_name.index(read_msg)]
             now_data_time=data_time[data_name.index(read_msg)]
             now_data_des=data_des[data_name.index(read_msg)]
threading.Thread(target=get_arduino,daemon=True).start()

app = Flask(__name__)

@app.route('/api',)
def get_api():
    req = requests.get('http://dnd5eapi.co/api/conditions/blinded')
    print(req.content)
    api_data = json.loads(req)
    return render_template("main.html",api_data=api_data) 

@app.route('/data', methods=['GET', 'POST'])
def read_data():
    global is_start
    datas={}
    num=1
    datas["now_data_name"]=now_data_name
    datas["now_data_time"]=now_data_time
    datas["now_data_des"]=now_data_des
    datas["is_start"]=is_start
    return datas

@app.route('/start', methods=['GET', 'POST'])
def set_data():
    global is_start
    is_start=1
    datas={}
    return datas
@app.route('/buzzer_on', methods=['GET', 'POST'])
def reset_data():
    global is_start,serialcom
    serialcom.write("on".encode())
    is_start=0
    datas={}
    return datas
@app.route('/buzzer_off', methods=['GET', 'POST'])
def reset2_data():
    global is_start,serialcom
    serialcom.write("off".encode())
    is_start=0
    datas={}
    return datas
@app.route('/',methods=["GET"])
def main():
    req = requests.get('http://dnd5eapi.co/api/conditions/blinded')
    data=req.content
    print(req.content)
    return render_template("main.html",data=data)
@app.route('/main.html')
def gohome():

     return render_template("main.html")

if __name__ == '__main__':
    app.run(debug=True)

