from flask import Flask, render_template, request, redirect, url_for
import modbus_tk.defines as pdu
import modbus_tk.modbus_tcp as modbus_tcp
from paho.mqtt import client as mqtt

import uuid
import json
import time

# sever = modbus_tcp.TcpMaster('192.168.1.125', 20108)
sever = modbus_tcp.TcpMaster('192.168.1.132', 20105)
sever.set_timeout(5.0)
app = Flask(__name__)


def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
    else:
        print('Bad connection. Code:', rc)
        mqtt_publish()


def mqtt_connect():
    """连接MQTT服务器"""
    mqttClient = mqtt.Client(str(uuid.uuid4()))
    mqttClient.on_connect = handle_connect  # 返回连接状态的回调函数
    MQTTHOST = "192.168.1.219"  # MQTT服务器地址
    MQTTPORT = 1883  # MQTT端口
    mqttClient.username_pw_set("admin", "admin123")  # MQTT服务器账号密码, 无密码时注释即可
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()  # 启用线程连接

    return mqttClient


def mqtt_publish():
    mqttClient = mqtt_connect()
    PDUDevice1()
    text = [PDU.hardwareVer, PDU.softwareVer, PDU.deviveAdress, PDU.baudRate, PDU.Temperature, PDU.Humidity,
            PDU.transformer, PDU.transformer1, PDU.Tvoltage, PDU.Tcurrent, PDU.Tpower, PDU.Telectrical,
            PDU.Tcurrent1, PDU.Tpower1, PDU.Telectrical1, PDU.Tcurrent2, PDU.Tpower2, PDU.Telectrical2,
            PDU.Tcurrent3, PDU.Tpower3, PDU.Telectrical3, PDU.Tcurrent4, PDU.Tpower4, PDU.Telectrical4,
            PDU.Tcurrent5, PDU.Tpower5, PDU.Telectrical5, PDU.Tcurrent6, PDU.Tpower6, PDU.Telectrical6,
            PDU.Tcurrent7, PDU.Tpower7, PDU.Telectrical7, PDU.Tcurrent8, PDU.Tpower8, PDU.Telectrical8,
            PDU.Undervoltage, PDU.Overvoltage, PDU.Tovercurrent, PDU.Boverflow, PDU.TPthreshold,
            PDU.Bpthreshold, PDU.Utlimit, PDU.Ltlimit, PDU.Uhlimit, PDU.Lhlimit]
    pduwr = json.dumps(text, ensure_ascii=False)
    mqttClient.publish('/PDU/RX', pduwr, 2)
    mqttClient.loop_start()


class device:
    def __init__(self):
        self.hardwareVer = 0,
        self.softwareVer = 0,
        self.deviveAdress = 0,
        self.baudRate = 0,
        # 温湿度
        self.Temperature = 0,
        self.Humidity = 0,
        # 总输入互感器变比，支路互感器变比
        self.transformer = 0,
        self.transformer1 = 0,
        # 总电路
        self.Tvoltage = 0,
        self.Tcurrent = 0,
        self.Tpower = 0,
        self.Telectrical = 0,
        # 支路一
        self.Tcurrent1 = 0,
        self.Tpower1 = 0,
        self.Telectrical1 = 0,
        # 支路二
        self.Tcurrent2 = 0,
        self.Tpower2 = 0,
        self.Telectrical2 = 0,
        # 支路三
        self.Tcurrent3 = 0,
        self.Tpower3 = 0,
        self.Telectrical3 = 0,
        # 支路四
        self.Tcurrent4 = 0,
        self.Tpower4 = 0,
        self.Telectrical4 = 0,
        # 支路五
        self.Tcurrent5 = 0,
        self.Tpower5 = 0,
        self.Telectrical5 = 0,
        # 支路六
        self.Tcurrent6 = 0,
        self.Tpower6 = 0,
        self.Telectrical6 = 0,
        # 支路七
        self.Tcurrent7 = 0,
        self.Tpower7 = 0,
        self.Telectrical7 = 0,
        # 支路八
        self.Tcurrent8 = 0,
        self.Tpower8 = 0,
        self.Telectrical8 = 0,
        # 温湿度报警标记
        self.HTalarm = 0
        # 欠压过压阀值
        self.Undervoltage = 0
        self.Overvoltage = 0
        # 总、支路过流报警阀值
        self.Tovercurrent = 0
        self.Boverflow = 0
        # 总、支路功率告警阀值
        self.TPthreshold = 0
        self.Bpthreshold = 0
        # 温度湿度上下限
        self.Utlimit = 0
        self.Ltlimit = 0
        self.Uhlimit = 0
        self.Lhlimit = 0
        # 烟感、水浸、防雷传感器告警记录
        self.Smoke = 0
        self.water = 0
        self.Plightning = 0
        # 防雷计数器告警次数次数
        self.Plfrequency = 0


PDU = device()


# OneOpen:257  OneClose:256
# TwoOpen:513  TwoClose:512
# ThreeOpen:769  ThreeClose:768
# FourOpen:1025  FourClose:1024
# FiveOpen:1281  FiveClose:1280
# SixOpen:1537  SixClose:1536
# SevenOpen:1793  SevenClose:1792
# EightOpen:2049  EightClose:2048
def switchStatus(outputValue):
    sever.execute(241, pdu.WRITE_SINGLE_REGISTER, 170, output_value=outputValue)


def ReadPDU(deviceid, adress, length):
    return sever.execute(deviceid, pdu.READ_HOLDING_REGISTERS, adress, length)


@app.route('/')
def main():
    return render_template('index.html')


# @app.route('/')  # HTTP超时延迟
# def make_request(requests=None):
#     try:
#         response = requests.get('http://192.168.1.132:20105', timeout=5)
#         # 在5秒内接收到响应
#         return response.text
#     except requests.Timeout:
#         # 请求超时
#         return 'Request timed out'
#     except requests.RequestException:
#         # 请求异常
#         return 'Request exception occurred'


@app.route('/PDU_scoket')
def PDU_scoket():
    status = "{:08b}".format(ReadPDU(241, 157, 1)[0])
    socket_list = [int(i) for element in status for i in element]
    return render_template('PDU_scoket.html', socket_list=socket_list)


@app.route('/PDUDevice')
def PDUDevice():
    hardwareVer = int("{:0x}".format(ReadPDU(241, 0, 1)[0]))
    PDU.hardwareVer = str(int(hardwareVer / 1000)) + "." + str(
        int((hardwareVer % 1000) / 100)) + "." + str(
        hardwareVer % 100)
    softwareVer = int("{:0x}".format(ReadPDU(241, 1, 1)[0]))
    PDU.softwareVer = str(int(softwareVer / 1000)) + "." + str(int((softwareVer % 1000) / 100)) + "." + str(
        softwareVer % 100)
    PDU.deviveAdress = "{:0x}".format(ReadPDU(241, 2, 1)[0])
    PDU.baudRate = "{:0x}".format(ReadPDU(241, 3, 2)[0] + ReadPDU(241, 3, 2)[1])

    Temperature = int("{:0x}".format(ReadPDU(241, 128, 1)[0]))
    PDU.Temperature = str(Temperature / 100) + "\u2103"
    Humidity = int("{:0x}".format(ReadPDU(241, 129, 1)[0]))
    PDU.Humidity = str(Humidity / 100) + "%RH"
    # 总输入互感器变比，支路互感器变比
    PDU.transformer = str("{:0x}".format(ReadPDU(241, 5, 1)[0]) + ":1")
    PDU.transformer1 = str("{:0x}".format(ReadPDU(241, 6, 1)[0]) + ":1")

    # 总电压，总电流，总功率，总电能
    Tvoltage = "{:0x}".format(ReadPDU(241, 7, 2)[0]) + "{:0x}".format(ReadPDU(241, 7, 2)[1])
    PDU.Tvoltage = str(int(Tvoltage) / 100) + "V"
    Tcurrent = "{:0x}".format(ReadPDU(241, 9, 2)[0]) + "{:0x}".format(ReadPDU(241, 9, 2)[1])
    PDU.Tcurrent = str(int(Tcurrent) / 100) + "A"
    Tpower = "{:0x}".format(ReadPDU(241, 11, 2)[0]) + "{:0x}".format(ReadPDU(241, 11, 2)[1])
    PDU.Tpower = str(int(Tpower) / 100) + "KW"
    Telectrica = "{:0x}".format(ReadPDU(241, 13, 3)[0]) + "{:0x}".format(ReadPDU(241, 13, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 13, 3)[2])
    PDU.Telectrical = str(int(Telectrica) / 1000) + "KWH"

    return render_template('PDUDevice.html', PDU=PDU)


def PDUDevice1():
    hardwareVer = int("{:0x}".format(ReadPDU(241, 0, 1)[0]))
    PDU.hardwareVer = str(int(hardwareVer / 1000)) + "." + str(
        int((hardwareVer % 1000) / 100)) + "." + str(
        hardwareVer % 100)
    softwareVer = int("{:0x}".format(ReadPDU(241, 1, 1)[0]))
    PDU.softwareVer = str(int(softwareVer / 1000)) + "." + str(int((softwareVer % 1000) / 100)) + "." + str(
        softwareVer % 100)
    PDU.deviveAdress = "{:0x}".format(ReadPDU(241, 2, 1)[0])
    PDU.baudRate = "{:0x}".format(ReadPDU(241, 3, 2)[0] + ReadPDU(241, 3, 2)[1])

    Temperature = int("{:0x}".format(ReadPDU(241, 128, 1)[0]))
    PDU.Temperature = str(Temperature / 100) + "\u2103"
    Humidity = int("{:0x}".format(ReadPDU(241, 129, 1)[0]))
    PDU.Humidity = str(Humidity / 100) + "%RH"
    # 总输入互感器变比，支路互感器变比
    PDU.transformer = str("{:0x}".format(ReadPDU(241, 5, 1)[0]) + ":1")
    PDU.transformer1 = str("{:0x}".format(ReadPDU(241, 6, 1)[0]) + ":1")

    # 总电压，总电流，总功率，总电能
    Tvoltage = "{:0x}".format(ReadPDU(241, 7, 2)[0]) + "{:0x}".format(ReadPDU(241, 7, 2)[1])
    PDU.Tvoltage = str(int(Tvoltage) / 100) + "V"
    Tcurrent = "{:0x}".format(ReadPDU(241, 9, 2)[0]) + "{:0x}".format(ReadPDU(241, 9, 2)[1])
    PDU.Tcurrent = str(int(Tcurrent) / 100) + "A"
    Tpower = "{:0x}".format(ReadPDU(241, 11, 2)[0]) + "{:0x}".format(ReadPDU(241, 11, 2)[1])
    PDU.Tpower = str(int(Tpower) / 100) + "KW"
    Telectrica = "{:0x}".format(ReadPDU(241, 13, 3)[0]) + "{:0x}".format(ReadPDU(241, 13, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 13, 3)[2])
    PDU.Telectrical = str(int(Telectrica) / 1000) + "KWH"

    Tcurrent1 = "{:0x}".format(ReadPDU(241, 16, 2)[0]) + "{:0x}".format(ReadPDU(241, 16, 2)[1])
    PDU.Tcurrent1 = str(int(Tcurrent1) / 1000) + "A"
    Tpower1 = "{:0x}".format(ReadPDU(241, 18, 2)[0]) + "{:0x}".format(ReadPDU(241, 18, 2)[1])
    PDU.Tpower1 = str(int(Tpower1[-5:]) / 10) + "W"
    Telectrica1 = "{:0x}".format(ReadPDU(241, 20, 3)[0]) + "{:0x}".format(ReadPDU(241, 20, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 20, 3)[2])
    PDU.Telectrical1 = str(int(Telectrica1) / 1000) + "KWH"

    # 电流，功率，电能(支路2）

    Tcurrent2 = "{:0x}".format(ReadPDU(241, 23, 2)[0]) + "{:0x}".format(ReadPDU(241, 23, 2)[1])
    PDU.Tcurrent2 = str(int(Tcurrent2) / 1000) + "A"
    Tpower2 = "{:0x}".format(ReadPDU(241, 25, 2)[0]) + "{:0x}".format(ReadPDU(241, 25, 2)[1])
    PDU.Tpower2 = str(int(Tpower2[-5:]) / 10) + "W"
    Telectrica2 = "{:0x}".format(ReadPDU(241, 27, 3)[0]) + "{:0x}".format(ReadPDU(241, 27, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 27, 3)[2])
    PDU.Telectrical2 = str(int(Telectrica2) / 1000) + "KWH"

    # 电流，功率，电能(支路3）

    Tcurrent3 = "{:0x}".format(ReadPDU(241, 30, 2)[0]) + "{:0x}".format(ReadPDU(241, 30, 2)[1])
    PDU.Tcurrent3 = str(int(Tcurrent3) / 1000) + "A"
    Tpower3 = "{:0x}".format(ReadPDU(241, 32, 2)[0]) + "{:0x}".format(ReadPDU(241, 32, 2)[1])
    PDU.Tpower3 = str(int(Tpower3[-5:]) / 10) + "W"
    Telectrica3 = "{:0x}".format(ReadPDU(241, 34, 3)[0]) + "{:0x}".format(ReadPDU(241, 34, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 34, 3)[2])
    PDU.Telectrical3 = str(int(Telectrica3) / 1000) + "KWH"

    # 电流，功率，电能(支路4）

    Tcurrent4 = "{:0x}".format(ReadPDU(241, 37, 2)[0]) + "{:0x}".format(ReadPDU(241, 37, 2)[1])
    PDU.Tcurrent4 = str(int(Tcurrent4) / 1000) + "A"
    Tpower4 = "{:0x}".format(ReadPDU(241, 39, 2)[0]) + "{:0x}".format(ReadPDU(241, 39, 2)[1])
    PDU.Tpower4 = str(int(Tpower4[-5:]) / 10) + "W"
    Telectrica4 = "{:0x}".format(ReadPDU(241, 41, 3)[0]) + "{:0x}".format(ReadPDU(241, 41, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 41, 3)[2])
    PDU.Telectrical4 = str(int(Telectrica4) / 1000) + "KWH"

    # 电流，功率，电能(支路5）

    Tcurrent5 = "{:0x}".format(ReadPDU(241, 44, 2)[0]) + "{:0x}".format(ReadPDU(241, 44, 2)[1])
    PDU.Tcurrent5 = str(int(Tcurrent5) / 1000) + "A"
    Tpower5 = "{:0x}".format(ReadPDU(241, 46, 2)[0]) + "{:0x}".format(ReadPDU(241, 46, 2)[1])
    PDU.Tpower5 = str(int(Tpower5[-5:]) / 10) + "W"
    Telectrica5 = "{:0x}".format(ReadPDU(241, 48, 3)[0]) + "{:0x}".format(ReadPDU(241, 48, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 48, 3)[2])
    PDU.Telectrical5 = str(int(Telectrica5) / 1000) + "KWH"

    # 电流，功率，电能(支路6）

    Tcurrent6 = "{:0x}".format(ReadPDU(241, 51, 2)[0]) + "{:0x}".format(ReadPDU(241, 51, 2)[1])
    PDU.Tcurrent6 = str(int(Tcurrent6) / 1000) + "A"
    Tpower6 = "{:0x}".format(ReadPDU(241, 53, 2)[0]) + "{:0x}".format(ReadPDU(241, 53, 2)[1])
    PDU.Tpower6 = str(int(Tpower6[-5:]) / 10) + "W"
    Telectrica6 = "{:0x}".format(ReadPDU(241, 55, 3)[0]) + "{:0x}".format(ReadPDU(241, 55, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 55, 3)[2])
    PDU.Telectrical6 = str(int(Telectrica6) / 1000) + "KWH"

    # 电流，功率，电能(支路7）

    Tcurrent7 = "{:0x}".format(ReadPDU(241, 58, 2)[0]) + "{:0x}".format(ReadPDU(241, 58, 2)[1])
    PDU.Tcurrent7 = str(int(Tcurrent7) / 1000) + "A"
    Tpower7 = "{:0x}".format(ReadPDU(241, 60, 2)[0]) + "{:0x}".format(ReadPDU(241, 60, 2)[1])
    PDU.Tpower7 = str(int(Tpower7[-5:]) / 10) + "W"
    Telectrica7 = "{:0x}".format(ReadPDU(241, 62, 3)[0]) + "{:0x}".format(ReadPDU(241, 62, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 62, 3)[2])
    PDU.Telectrical7 = str(int(Telectrica7) / 1000) + "KWH"

    # 电流，功率，电能(支路8）

    Tcurrent8 = "{:0x}".format(ReadPDU(241, 65, 2)[0]) + "{:0x}".format(ReadPDU(241, 65, 2)[1])
    PDU.Tcurrent8 = str(int(Tcurrent8) / 1000) + "A"
    Tpower8 = "{:0x}".format(ReadPDU(241, 67, 2)[0]) + "{:0x}".format(ReadPDU(241, 67, 2)[1])
    PDU.Tpower8 = str(int(Tpower8[-5:]) / 10) + "W"
    Telectrica8 = "{:0x}".format(ReadPDU(241, 69, 3)[0]) + "{:0x}".format(ReadPDU(241, 69, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 69, 3)[2])
    PDU.Telectrical8 = str(int(Telectrica8) / 1000) + "KWH"

    # 温湿度报警标记
    HTalarm = "{:0X}".format(ReadPDU(241, 130, 1)[0])
    HTalarm1 = int(HTalarm[:2])  # 高八位
    HTalarm2 = int(HTalarm[-2:])  # 低八位
    if HTalarm1 == 10:
        if HTalarm2 == 10:
            PDU.HTalarm = "此时温度低于下限，湿度低于下限"
        elif HTalarm2 == 11:
            PDU.HTalarm = "此时温度低于下限，湿度高于上限"
    if HTalarm == 11:
        if HTalarm2 == 10:
            PDU.HTalarm = "此时温度高于上限，湿度低于下限"
        if HTalarm2 == 11:
            PDU.HTalarm = "此时温度高于上限，湿度高于上限"
    else:
        PDU.HTalarm = "温度湿度一切正常"

    # 欠压阀值
    Undervoltage = "{:0X}".format(ReadPDU(241, 131, 1)[0])
    if 0 < int(Undervoltage) / 10 < 255:
        PDU.Undervoltage = str(int(Undervoltage) / 10) + "V"
    # 过压阀值
    Overvoltage = "{:0X}".format(ReadPDU(241, 132, 1)[0])
    if 0 < int(Overvoltage) / 10 < 255:
        PDU.Overvoltage = str(int(Overvoltage) / 10) + "V"

    # 总过流报警阀值
    Tovercurrent = "{:0X}".format(ReadPDU(241, 133, 1)[0])
    PDU.Tovercurrent = str(int(Tovercurrent) / 100) + "A"

    # 支路过流报警阀值
    Boverflow = "{:0X}".format(ReadPDU(241, 134, 1)[0])
    PDU.Boverflow = str(int(Boverflow) / 100) + "A"

    # 总有功功率告警阈值
    TPthoreshold = "{:0X}".format(ReadPDU(241, 135, 1)[0])
    if 0 < int(TPthoreshold) / 100 < 99.99:
        PDU.TPthreshold = str(int(TPthoreshold) / 100) + "KW"

    # 支路功率告警阀值
    Bpthreshold = "{:0X}".format(ReadPDU(241, 136, 1)[0])
    if 0 < int(Bpthreshold) / 100 < 99.99:
        PDU.Bpthreshold = str(int(Bpthreshold) / 100) + "KW"

    # 温度上限
    Utlimit = "{:0X}".format(ReadPDU(241, 137, 1)[0])
    if 0 < int(Utlimit) / 100 < 99.99:
        PDU.Utlimit = str(int(Utlimit) / 100) + "\u2103"
    # 温度下限
    Ltlimit = "{:0X}".format(ReadPDU(241, 138, 1)[0])
    if 0 < int(Ltlimit) / 100 < 99.99:
        PDU.Ltlimit = str(int(Ltlimit) / 100) + "\u2103"

    # 湿度上限
    Uhlimit = "{:0X}".format(ReadPDU(241, 139, 1)[0])
    if 0 < int(Uhlimit) / 100 < 99.99:
        PDU.Uhlimit = str(int(Uhlimit) / 100) + "%Rh"
    # 湿度下限
    Lhlimit = "{:0X}".format(ReadPDU(241, 140, 1)[0])
    if 0 < int(Lhlimit) / 100 < 99.99:
        PDU.Lhlimit = str(int(Lhlimit) / 100) + "%Rh"
    return


@app.route('/PDUBranch')
def PDUBranch():
    # 电流，功率，电能(支路1）

    Tcurrent1 = "{:0x}".format(ReadPDU(241, 16, 2)[0]) + "{:0x}".format(ReadPDU(241, 16, 2)[1])
    PDU.Tcurrent1 = str(int(Tcurrent1) / 1000) + "A"
    Tpower1 = "{:0x}".format(ReadPDU(241, 18, 2)[0]) + "{:0x}".format(ReadPDU(241, 18, 2)[1])
    PDU.Tpower1 = str(int(Tpower1[-5:]) / 10) + "W"
    Telectrica1 = "{:0x}".format(ReadPDU(241, 20, 3)[0]) + "{:0x}".format(ReadPDU(241, 20, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 20, 3)[2])
    PDU.Telectrical1 = str(int(Telectrica1) / 1000) + "KWH"

    # 电流，功率，电能(支路2）

    Tcurrent2 = "{:0x}".format(ReadPDU(241, 23, 2)[0]) + "{:0x}".format(ReadPDU(241, 23, 2)[1])
    PDU.Tcurrent2 = str(int(Tcurrent2) / 1000) + "A"
    Tpower2 = "{:0x}".format(ReadPDU(241, 25, 2)[0]) + "{:0x}".format(ReadPDU(241, 25, 2)[1])
    PDU.Tpower2 = str(int(Tpower2[-5:]) / 10) + "W"
    Telectrica2 = "{:0x}".format(ReadPDU(241, 27, 3)[0]) + "{:0x}".format(ReadPDU(241, 27, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 27, 3)[2])
    PDU.Telectrical2 = str(int(Telectrica2) / 1000) + "KWH"

    # 电流，功率，电能(支路3）

    Tcurrent3 = "{:0x}".format(ReadPDU(241, 30, 2)[0]) + "{:0x}".format(ReadPDU(241, 30, 2)[1])
    PDU.Tcurrent3 = str(int(Tcurrent3) / 1000) + "A"
    Tpower3 = "{:0x}".format(ReadPDU(241, 32, 2)[0]) + "{:0x}".format(ReadPDU(241, 32, 2)[1])
    PDU.Tpower3 = str(int(Tpower3[-5:]) / 10) + "W"
    Telectrica3 = "{:0x}".format(ReadPDU(241, 34, 3)[0]) + "{:0x}".format(ReadPDU(241, 34, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 34, 3)[2])
    PDU.Telectrical3 = str(int(Telectrica3) / 1000) + "KWH"

    # 电流，功率，电能(支路4）

    Tcurrent4 = "{:0x}".format(ReadPDU(241, 37, 2)[0]) + "{:0x}".format(ReadPDU(241, 37, 2)[1])
    PDU.Tcurrent4 = str(int(Tcurrent4) / 1000) + "A"
    Tpower4 = "{:0x}".format(ReadPDU(241, 39, 2)[0]) + "{:0x}".format(ReadPDU(241, 39, 2)[1])
    PDU.Tpower4 = str(int(Tpower4[-5:]) / 10) + "W"
    Telectrica4 = "{:0x}".format(ReadPDU(241, 41, 3)[0]) + "{:0x}".format(ReadPDU(241, 41, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 41, 3)[2])
    PDU.Telectrical4 = str(int(Telectrica4) / 1000) + "KWH"

    # 电流，功率，电能(支路5）

    Tcurrent5 = "{:0x}".format(ReadPDU(241, 44, 2)[0]) + "{:0x}".format(ReadPDU(241, 44, 2)[1])
    PDU.Tcurrent5 = str(int(Tcurrent5) / 1000) + "A"
    Tpower5 = "{:0x}".format(ReadPDU(241, 46, 2)[0]) + "{:0x}".format(ReadPDU(241, 46, 2)[1])
    PDU.Tpower5 = str(int(Tpower5[-5:]) / 10) + "W"
    Telectrica5 = "{:0x}".format(ReadPDU(241, 48, 3)[0]) + "{:0x}".format(ReadPDU(241, 48, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 48, 3)[2])
    PDU.Telectrical5 = str(int(Telectrica5) / 1000) + "KWH"

    # 电流，功率，电能(支路6）

    Tcurrent6 = "{:0x}".format(ReadPDU(241, 51, 2)[0]) + "{:0x}".format(ReadPDU(241, 51, 2)[1])
    PDU.Tcurrent6 = str(int(Tcurrent6) / 1000) + "A"
    Tpower6 = "{:0x}".format(ReadPDU(241, 53, 2)[0]) + "{:0x}".format(ReadPDU(241, 53, 2)[1])
    PDU.Tpower6 = str(int(Tpower6[-5:]) / 10) + "W"
    Telectrica6 = "{:0x}".format(ReadPDU(241, 55, 3)[0]) + "{:0x}".format(ReadPDU(241, 55, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 55, 3)[2])
    PDU.Telectrical6 = str(int(Telectrica6) / 1000) + "KWH"

    # 电流，功率，电能(支路7）

    Tcurrent7 = "{:0x}".format(ReadPDU(241, 58, 2)[0]) + "{:0x}".format(ReadPDU(241, 58, 2)[1])
    PDU.Tcurrent7 = str(int(Tcurrent7) / 1000) + "A"
    Tpower7 = "{:0x}".format(ReadPDU(241, 60, 2)[0]) + "{:0x}".format(ReadPDU(241, 60, 2)[1])
    PDU.Tpower7 = str(int(Tpower7[-5:]) / 10) + "W"
    Telectrica7 = "{:0x}".format(ReadPDU(241, 62, 3)[0]) + "{:0x}".format(ReadPDU(241, 62, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 62, 3)[2])
    PDU.Telectrical7 = str(int(Telectrica7) / 1000) + "KWH"

    # 电流，功率，电能(支路8）

    Tcurrent8 = "{:0x}".format(ReadPDU(241, 65, 2)[0]) + "{:0x}".format(ReadPDU(241, 65, 2)[1])
    PDU.Tcurrent8 = str(int(Tcurrent8) / 1000) + "A"
    Tpower8 = "{:0x}".format(ReadPDU(241, 67, 2)[0]) + "{:0x}".format(ReadPDU(241, 67, 2)[1])
    PDU.Tpower8 = str(int(Tpower8[-5:]) / 10) + "W"
    Telectrica8 = "{:0x}".format(ReadPDU(241, 69, 3)[0]) + "{:0x}".format(ReadPDU(241, 69, 3)[1]) + "{:0x}".format(
        ReadPDU(241, 69, 3)[2])
    PDU.Telectrical8 = str(int(Telectrica8) / 1000) + "KWH"
    return render_template('PDUBranch.html', PDU=PDU)


##数据写入
# def PDUWrite():
#     if (Undervoltage1 is not None):
#         if 0 < int(Undervoltag1)*10 < 9999:
#             Undervoltage2 = int(str(Undervoltage1 * 10)[0]) * 16 ^ 3 + int(str(Undervoltage1 * 10)[1]) * 16 ^ 2 + int(
#                 str(Undervoltage1 * 10)[2]) * 16 ^ 1 + int(str(Undervoltage1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 131, output_value=Undervoltage2)
#     if (Overvoltage1 is not None):
#         if 0 < int(Overvoltage1)*10 < 9999:
#             Overvoltage2 = int(str(Overvoltage1 * 10)[0]) * 16 ^ 3 + int(str(Overvoltage1 * 10)[1]) * 16 ^ 2 + int(
#                 str(Overvoltage1 * 10)[2]) * 16 ^ 1 + int(str(Overvoltage1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 132, output_value=Overvoltage2)
#     if (Tovercurrent1 is not None):
#         if 0 < int(Tovercurrent1)*10 < 9999:
#             Tovercurrent2 = int(str(Tovercurrent1 * 10)[0]) * 16 ^ 3 + int(str(Tovercurrent1 * 10)[1]) * 16 ^ 2 + int(
#                 str(Tovercurrent1 * 10)[2]) * 16 ^ 1 + int(str(Tovercurrent1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 133, output_value=Tovercurrent2)
#     if (Boverflow1 is not None):
#         if 0 < int(Boverflow1)*10 < 9999:
#             Boverflow2 = int(str(Boverflow1 * 10)[0]) * 16 ^ 3 + int(str(Boverflow1 * 10)[1]) * 16 ^ 2 + int(
#                 str(Boverflow1 * 10)[2]) * 16 ^ 1 + int(str(Boverflow1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 134, output_value=Boverflow2)
#     if (TPthoreshold1 is not None):
#         if 0 < int(TPthoreshold1)*10 < 9999:
#             TPthoreshold2 = int(str(TPthoreshold1 * 10)[0]) * 16 ^ 3 + int(str(TPthoreshold1 * 10)[1]) * 16 ^ 2 + int(
#                 str(TPthoreshold1 * 10)[2]) * 16 ^ 1 + int(str(TPthoreshold1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 135, output_value=TPthoreshold2)
#     if (Bpthreshold1 is not None):
#         if 0 < int(Bpthreshold1)*10 < 9999:
#             Bpthreshold2 = int(str(Bpthreshold1 * 10)[0]) * 16 ^ 3 + int(str(Bpthreshold1 * 10)[1]) * 16 ^ 2 + int(
#                 str(Bpthreshold1 * 10)[2]) * 16 ^ 1 + int(str(Bpthreshold1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 136, output_value=Bpthreshold2)
#     if (Utlimit1 is not None):
#         if 0 < int(Utlimit1)*10 < 9999:
#             Utlimit2 = int(str(Utlimit1 * 10)[0]) * 16 ^ 3 + int(str(Utlimit1 * 10)[1]) * 16 ^ 2 + int(
#                 str(Utlimit1 * 10)[2]) * 16 ^ 1 + int(str(Utlimit1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 137, output_value=Utlimit2)
#     if (Ltlimit1 is not None):
#         if 0 < int(Ltlimit1)*10 < 9999:
#             Ltlimit2 = int(str(Ltlimit1 * 10)[0]) * 16 ^ 3 + int(str(Ltlimit1 * 10)[1]) * 16 ^ 2 + int(
#                 str(Ltlimit1 * 10)[2]) * 16 ^ 1 + int(str(Ltlimit1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 138, output_value=Ltlimit2)
#     if (Uhlimit1 is not None):
#         if 0 < int(Uhlimit1)*10 < 9999:
#             Uhlimit2 = int(str(Uhlimit1 * 10)[0]) * 16 ^ 3 + int(str(Uhlimit1 * 10)[1]) * 16 ^ 2 + int(
#                 str(Uhlimit1 * 10)[2]) * 16 ^ 1 + int(str(Uhlimit1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 139, output_value=Uhlimit2)
#     if (Lhlimit1 is not None):
#         if 0 < int(Lhlimit1)*10 < 9999:
#             Lhlimit2 = int(str(Lhlimit1 * 10)[0]) * 16 ^ 3 + int(str(Lhlimit1 * 10)[1]) * 16 ^ 2 + int(
#                 str(Lhlimit1 * 10)[2]) * 16 ^ 1 + int(str(Lhlimit1 * 10)[3]) * 16 ^ 0
#         sever.execute(241, 6, 140, output_value=Lhlimit2)


@app.route('/PDUAlert')
def PDUAlert():
    # 温湿度报警标记
    HTalarm = "{:0X}".format(ReadPDU(241, 130, 1)[0])
    HTalarm1 = int(HTalarm[:2])  # 高八位
    HTalarm2 = int(HTalarm[-2:])  # 低八位
    if HTalarm1 == 10:
        if HTalarm2 == 10:
            PDU.HTalarm = "此时温度低于下限，湿度低于下限"
        elif HTalarm2 == 11:
            PDU.HTalarm = "此时温度低于下限，湿度高于上限"
    if HTalarm == 11:
        if HTalarm2 == 10:
            PDU.HTalarm = "此时温度高于上限，湿度低于下限"
        if HTalarm2 == 11:
            PDU.HTalarm = "此时温度高于上限，湿度高于上限"
    else:
        PDU.HTalarm = "温度湿度一切正常"

    # 欠压阀值
    Undervoltage = "{:0X}".format(ReadPDU(241, 131, 1)[0])
    if 0 < int(Undervoltage) / 10 < 255:
        PDU.Undervoltage = str(int(Undervoltage) / 10) + "V"
    # 过压阀值
    Overvoltage = "{:0X}".format(ReadPDU(241, 132, 1)[0])
    if 0 < int(Overvoltage) / 10 < 255:
        PDU.Overvoltage = str(int(Overvoltage) / 10) + "V"

    # 总过流报警阀值
    Tovercurrent = "{:0X}".format(ReadPDU(241, 133, 1)[0])
    PDU.Tovercurrent = str(int(Tovercurrent) / 100) + "A"

    # 支路过流报警阀值
    Boverflow = "{:0X}".format(ReadPDU(241, 134, 1)[0])
    PDU.Boverflow = str(int(Boverflow) / 100) + "A"

    # 总有功功率告警阈值
    TPthoreshold = "{:0X}".format(ReadPDU(241, 135, 1)[0])
    if 0 < int(TPthoreshold) / 100 < 99.99:
        PDU.TPthreshold = str(int(TPthoreshold) / 100) + "KW"

    # 支路功率告警阀值
    Bpthreshold = "{:0X}".format(ReadPDU(241, 136, 1)[0])
    if 0 < int(Bpthreshold) / 100 < 99.99:
        PDU.Bpthreshold = str(int(Bpthreshold) / 100) + "KW"

    # 温度上限
    Utlimit = "{:0X}".format(ReadPDU(241, 137, 1)[0])
    if 0 < int(Utlimit) / 100 < 99.99:
        PDU.Utlimit = str(int(Utlimit) / 100) + "\u2103"
    # 温度下限
    Ltlimit = "{:0X}".format(ReadPDU(241, 138, 1)[0])
    if 0 < int(Ltlimit) / 100 < 99.99:
        PDU.Ltlimit = str(int(Ltlimit) / 100) + "\u2103"

    # 湿度上限
    Uhlimit = "{:0X}".format(ReadPDU(241, 139, 1)[0])
    if 0 < int(Uhlimit) / 100 < 99.99:
        PDU.Uhlimit = str(int(Uhlimit) / 100) + "%Rh"
    # 湿度下限
    Lhlimit = "{:0X}".format(ReadPDU(241, 140, 1)[0])
    if 0 < int(Lhlimit) / 100 < 99.99:
        PDU.Lhlimit = str(int(Lhlimit) / 100) + "%Rh"

    # 烟感传感器告警记录
    Smoke = "{:0X}".format(ReadPDU(241, 147, 3)[0])
    Smoke1 = "{:0X}".format(ReadPDU(241, 147, 3)[1])
    Smoke2 = "{:0X}".format(ReadPDU(241, 147, 3)[2])
    if str(Smoke2[-2:]) == '00':
        PDU.Smoke = "烟感报警器无触发动作"
    if str(Smoke2[-2:]) == '0E':
        PDU.Smoke = str(Smoke[:2]) + "月" + str(Smoke[-2:]) + "日" + str(Smoke1[:2]) + "点" + str(
            Smoke1[-2:]) + "分" + str(
            Smoke2[:2]) + "秒" + "烟感报警器触发"

    # 水浸传感器告警记录
    water = "{:0X}".format(ReadPDU(241, 150, 3)[0])
    water1 = "{:0X}".format(ReadPDU(241, 150, 3)[1])
    water2 = "{:0X}".format(ReadPDU(241, 150, 3)[2])
    if str(water2[-2:]) == '00':
        PDU.water = "水浸报警器无触发动作"
    if str(water2[-2:]) == '0E':
        PDU.water = str(water[:2]) + "月" + str(water[-2:]) + "日" + str(water1[:2]) + "点" + str(
            water1[-2:]) + "分" + str(
            water2[:2]) + "秒" + "水浸报警器触发"

    # 防雷计数器告警记录，防雷计数器告警次数
    Plightning = "{:0X}".format(ReadPDU(241, 153, 3)[0])
    Plightning1 = "{:0X}".format(ReadPDU(241, 153, 3)[1])
    Plightning2 = "{:0X}".format(ReadPDU(241, 153, 3)[2])
    Plfrequency = "{:0X}".format(ReadPDU(241, 156, 1)[0])
    if str(Plightning2[-2:]) == '00':
        PDU.Plightning = "防雷计数器无触发动作"
        if 0 < int(Plfrequency) < 9999:
            PDU.Plfrequency = str(int(Plfrequency)) + "次"
    if str(Plightning2[-2:]) == '0E':
        PDU.Plightning = str(int(Plightning[:2])) + "月" + str(int(Plightning[-2:])) + "日" + str(
            int(Plightning1[:2])) + "点" + str(
            int(Plightning1[-2:])) + "分" + str(int(Plightning2[:2])) + "秒" + "防雷计数器触发"
        if 0 < int(Plfrequency) < 9999:
            PDU.Plfrequency = str(int(Plfrequency)) + "次"

    return render_template('PDUAlert.html', PDU=PDU)


@app.route('/', methods=['post'])
def PDUswitch():
    switch = int(request.form['switch_num'])
    switch_num = (switch // 10) % 10
    switch_action = switch % 10
    if switch_num == 0:
        output_value = 256 if switch_action == 1 else 257
        switchStatus(output_value)
    elif switch_num == 1:
        output_value = 512 if switch_action == 1 else 513
        switchStatus(output_value)
    elif switch_num == 2:
        output_value = 768 if switch_action == 1 else 769
        switchStatus(output_value)
    elif switch_num == 3:
        output_value = 1024 if switch_action == 1 else 1025
        switchStatus(output_value)
    elif switch_num == 4:
        output_value = 1280 if switch_action == 1 else 1281
        switchStatus(output_value)
    elif switch_num == 5:
        output_value = 1536 if switch_action == 1 else 1537
        switchStatus(output_value)
    elif switch_num == 6:
        output_value = 1792 if switch_action == 1 else 1793
        switchStatus(output_value)
    elif switch_num == 7:
        output_value = 2048 if switch_action == 1 else 2049
        switchStatus(output_value)
    else:
        return redirect(url_for('PDU_scoket'))
    return redirect(url_for('PDU_scoket'))


mqtt_publish()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010, debug=True)

