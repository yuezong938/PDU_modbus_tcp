import modbus_tk.defines as pdu
import modbus_tk.modbus_tcp as modbus_tcp

from paho.mqtt import client as mqtt
import uuid
import json


def on_connect(client, userdata, flags, rc):
    """
    一旦连接成功, 回调此方法
    rc的值表示成功与否：
        0:连接成功
        1:连接被拒绝-协议版本不正确
        2:连接被拒绝-客户端标识符无效
        3:连接被拒绝-服务器不可用
        4:连接被拒绝-用户名或密码不正确
        5:连接被拒绝-未经授权
        6-255:当前未使用。
    """
    rc_status = ["连接成功", "协议版本不正确", "客户端标识符无效", "服务器不可用", "用户名或密码不正确", "未经授权"]
    print("connect：", rc_status[rc])


def mqtt_connect():
    """连接MQTT服务器"""
    mqttClient = mqtt.Client(str(uuid.uuid4()))
    mqttClient.on_connect = on_connect  # 返回连接状态的回调函数
    MQTTHOST = "192.168.1.240"  # MQTT服务器地址
    MQTTPORT = 1883  # MQTT端口
    mqttClient.username_pw_set("mqtt", "mqttsisi")  # MQTT服务器账号密码, 无密码时注释即可
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()  # 启用线程连接

    return mqttClient


def mqtt_publish():
    """发布主题为'mqtt/demo',内容为'Demo text',服务质量为2"""
    mqttClient = mqtt_connect()
    # text = {PDU.HardwareVer, PDU.SoftwareVer, PDU.switchstatus, PDU.baudRate, PDU.Temperature, PDU.Humidity,
    #         PDU.transformer, PDU.Tvoltage, PDU.Tcurrent, PDU.Tpower, PDU.Telectrical}
    text = {"HardwareVer": str(PDU.HardwareVer)}
    pduwr = 'text.json'
    with open(pduwr, 'w', encoding='utf-8') as file_obj:
        json.dump(text, file_obj)
    mqttClient.publish('mqtt/demo', text, 2)
    mqttClient.loop_stop()


sever = modbus_tcp.TcpMaster('192.168.1.132', 20105)
sever.set_timeout(5.0)


class SN:
    def __init__(self):
        self.HardwareVer = 0
        self.SoftwareVer = 0
        self.switchstatus = 0
        self.baudRate = 0
        self.Temperature = 0
        self.Humidity = 0
        self.transformer = 0

        self.Tvoltage = 0
        self.Tcurrent = 0
        self.Tpower = 0
        self.Telectrical = 0
        #
        # self.Tcurrent1 = 0
        # self.Tpower1 = 0
        # self.Telectrical1 = 0
        #
        # self.Tcurrent2 = 0
        # self.Tpower2 = 0
        # self.Telectrical2 = 0
        #
        # self.Tcurrent3 = 0
        # self.Tpower3 = 0
        # self.Telectrical3 = 0
        #
        # self.Tcurrent4 = 0
        # self.Tpower4 = 0
        # self.Telectrical4 = 0
        #
        # self.Tcurrent5 = 0
        # self.Tpower5 = 0
        # self.Telectrical5 = 0
        #
        # self.Tcurrent6 = 0
        # self.Tpower6 = 0
        # self.Telectrical6 = 0
        #
        # self.Tcurrent7 = 0
        # self.Tpower7 = 0
        # self.Telectrical7 = 0
        #
        # self.Tcurrent8 = 0
        # self.Tpower8 = 0
        # self.Telectrical8 = 0

        # self.HTalarm = 0
        # self.Undervoltage = 0
        # self.Overvoltage = 0
        # self.Tovercurrent = 0
        # self.Boverflow = 0
        # self.TPthreshold = 0
        # self.Bpthreshold = 0
        # self.Utlimit = 0
        # self.Ltlimit = 0
        # self.Uhlimit = 0
        # self.Lhlimit = 0
        # self.Smoke = 0
        # self.water = 0
        # self.Plightning = 0
        # self.Plfrequency = 0


sever = modbus_tcp.TcpMaster('192.168.1.132', 20105)
sever.set_timeout(5.0)

PDU = SN()


def switchStatus(outputValue):
    sever.execute(241, pdu.WRITE_SINGLE_REGISTER, 170, output_value=outputValue)


def ReadPDU(deviceID, adress, length):
    return sever.execute(deviceID, pdu.READ_HOLDING_REGISTERS, adress, length)


# OneOpen:257  OneClose:256
# TwoOpen:513  TwoClose:512
# ThreeOpen:769  ThreeClose:768
# FourOpen:1025  FourClose:1024
# FiveOpen:1281  FiveClose:1280
# SixOpen:1537  SixClose:1536
# SevenOpen:1793  SevenClose:1792
# EightOpen:2049  EightClose:2048
# def switch(outputValue):
#     sever.execute(1, pdu.WRITE_SINGLE_REGISTER, 170, output_value=outputValue)


# 读插座状态
# PDU.switchstatus = sever.execute(1, pdu.READ_HOLDING_REGISTERS, 157, 1)
# PDU.HardwareVer = ReadPDU(1, 0, 1)

# print(PDU.HardwareVer[0])
# print(PDU.switchstatus[0])
# print("{0:b}".format(PDU.switchstatus[0]))
HardwareVer = int("{:0x}".format(ReadPDU(241, 0, 1)[0]))
PDU.HardwareVer = str(int(HardwareVer / 1000)) + "." + str((HardwareVer % 1000) / 100) + "." + str(HardwareVer % 100)
PDU.baudRate = "{:0x}".format(ReadPDU(241, 3, 2)[0] + ReadPDU(241, 3, 2)[1])
softwareVer = int("{:0x}".format(ReadPDU(241, 1, 1)[0]))
PDU.SoftwareVer = str(int(softwareVer / 1000)) + "." + str(int((softwareVer % 1000) / 100)) + "." + str(
    softwareVer % 100)
# 温湿度
Temperature = int("{:0x}".format(ReadPDU(241, 128, 1)[0]))
PDU.Temperature = str(Temperature / 100)
Humidity = int("{:0x}".format(ReadPDU(241, 129, 1)[0]))
PDU.Humidity = str(Humidity / 100)

# 总输入互感器变比，支路互感器变比
transformer = str("{:0x}".format(ReadPDU(241, 5, 1)[0]) + ":1")

transformer2 = str("{:0x}".format(ReadPDU(241, 6, 1)[0]) + ":1")

# 总电压，总电流，总功率，总电能
Tvoltage = "{:0x}".format(ReadPDU(241, 7, 2)[0]) + "{:0x}".format(ReadPDU(241, 7, 2)[1])
PDU.Tvoltage = int(Tvoltage) / 100
Tcurrent = "{:0x}".format(ReadPDU(241, 9, 2)[0]) + "{:0x}".format(ReadPDU(241, 9, 2)[1])
PDU.Tcurrent = int(Tcurrent) / 100
Tpower = "{:0x}".format(ReadPDU(241, 11, 2)[0]) + "{:0x}".format(ReadPDU(241, 11, 2)[1])
PDU.Tpower = int(Tpower) / 100
Telectrica = "{:0x}".format(ReadPDU(241, 13, 3)[0]) + "{:0x}".format(ReadPDU(241, 13, 3)[1]) + "{:0x}".format(
    ReadPDU(241, 13, 3)[2])
PDU.Telectrical = int(Telectrica) / 1000

# Tcurrent1 = "{:0x}".format(ReadPDU(241, 16, 2)[0]) + "{:0x}".format(ReadPDU(241, 16, 2)[1])
# PDU.Tcurrent1 = int(Tcurrent1) / 1000
# Tpower1 = "{:0x}".format(ReadPDU(241, 18, 2)[0]) + "{:0x}".format(ReadPDU(241, 18, 2)[1])
# PDU.Tpower1 = int(Tpower1) / 10
# Telectrica1 = "{:0x}".format(ReadPDU(241, 20, 3)[0]) + "{:0x}".format(ReadPDU(241, 20, 3)[1]) + "{:0x}".format(
#     ReadPDU(241, 20, 3)[2])
# PDU.Telectrical1 = int(Telectrica1) / 1000

# # 电流，功率，电能(支路2）
#
# Tcurrent2 = "{:0x}".format(ReadPDU(241, 23, 2)[0]) + "{:0x}".format(ReadPDU(241, 23, 2)[1])
# PDU.Tcurrent2 = int(Tcurrent2) / 1000
# Tpower2 = "{:0x}".format(ReadPDU(241, 25, 2)[0]) + "{:0x}".format(ReadPDU(241, 25, 2)[1])
# PDU.Tpower2 = int(Tpower2) / 10
# Telectrica2 = "{:0x}".format(ReadPDU(241, 27, 3)[0]) + "{:0x}".format(ReadPDU(241, 27, 3)[1]) + "{:0x}".format(
#     ReadPDU(241, 27, 3)[2])
# PDU.Telectrical2 = int(Telectrica2) / 1000

# 电流，功率，电能(支路3）

# Tcurrent3 = "{:0x}".format(ReadPDU(241, 30, 2)[0]) + "{:0x}".format(ReadPDU(241, 30, 2)[1])
# PDU.Tcurrent3 = int(Tcurrent3) / 1000
# Tpower3 = "{:0x}".format(ReadPDU(241, 32, 2)[0]) + "{:0x}".format(ReadPDU(241, 32, 2)[1])
# PDU.Tpower3 = int(Tpower3) / 10
# Telectrica3 = "{:0x}".format(ReadPDU(241, 34, 3)[0]) + "{:0x}".format(ReadPDU(241, 34, 3)[1]) + "{:0x}".format(
#     ReadPDU(241, 34, 3)[2])
# PDU.Telectrical3 = int(Telectrica3) / 1000
#
# # 电流，功率，电能(支路4）
#
# Tcurrent4 = "{:0x}".format(ReadPDU(241, 37, 2)[0]) + "{:0x}".format(ReadPDU(241, 37, 2)[1])
# PDU.Tcurrent4 = int(Tcurrent4) / 1000
# Tpower4 = "{:0x}".format(ReadPDU(241, 39, 2)[0]) + "{:0x}".format(ReadPDU(241, 39, 2)[1])
# PDU.Tpower4 = int(Tpower4[-5:]) / 10
# Telectrica4 = "{:0x}".format(ReadPDU(241, 41, 3)[0]) + "{:0x}".format(ReadPDU(241, 41, 3)[1]) + "{:0x}".format(
#     ReadPDU(241, 41, 3)[2])
# PDU.Telectrical4 = int(Telectrica4) / 1000

# 电流，功率，电能(支路5）

# Tcurrent5 = "{:0x}".format(ReadPDU(241, 44, 2)[0]) + "{:0x}".format(ReadPDU(241, 44, 2)[1])
# PDU.Tcurrent5 = int(Tcurrent5) / 1000
# Tpower5 = "{:0x}".format(ReadPDU(241, 46, 2)[0]) + "{:0x}".format(ReadPDU(241, 46, 2)[1])
# PDU.Tpower5 = int(Tpower5) / 10
# Telectrica5 = "{:0x}".format(ReadPDU(241, 48, 3)[0]) + "{:0x}".format(ReadPDU(241, 48, 3)[1]) + "{:0x}".format(
#     ReadPDU(241, 48, 3)[2])
# PDU.Telectrical5 = int(Telectrica5) / 1000
#
# # 电流，功率，电能(支路6）
#
# Tcurrent6 = "{:0x}".format(ReadPDU(241, 51, 2)[0]) + "{:0x}".format(ReadPDU(241, 51, 2)[1])
# PDU.Tcurrent6 = int(Tcurrent6) / 1000
# Tpower6 = "{:0x}".format(ReadPDU(241, 53, 2)[0]) + "{:0x}".format(ReadPDU(241, 53, 2)[1])
# PDU.Tpower6 = int(Tpower6) / 10
# Telectrica6 = "{:0x}".format(ReadPDU(241, 55, 3)[0]) + "{:0x}".format(ReadPDU(241, 55, 3)[1]) + "{:0x}".format(
#     ReadPDU(241, 55, 3)[2])
# PDU.Telectrical6 = int(Telectrica6) / 1000

# 电流，功率，电能(支路7）

# Tcurrent7 = "{:0x}".format(ReadPDU(241, 58, 2)[0]) + "{:0x}".format(ReadPDU(241, 58, 2)[1])
# PDU.Tcurrent7 = int(Tcurrent7) / 1000
# Tpower7 = "{:0x}".format(ReadPDU(241, 60, 2)[0]) + "{:0x}".format(ReadPDU(241, 60, 2)[1])
# PDU.Tpower7 = int(Tpower7) / 10
# Telectrica7 = "{:0x}".format(ReadPDU(241, 62, 3)[0]) + "{:0x}".format(ReadPDU(241, 62, 3)[1]) + "{:0x}".format(
#     ReadPDU(241, 62, 3)[2])
# PDU.Telectrical7 = int(Telectrica7) / 1000

# 电流，功率，电能(支路8）

# Tcurrent8 = "{:0x}".format(ReadPDU(241, 65, 2)[0]) + "{:0x}".format(ReadPDU(241, 65, 2)[1])
# PDU.Tcurrent8 = int(Tcurrent8) / 1000
# Tpower8 = "{:0x}".format(ReadPDU(241, 67, 2)[0]) + "{:0x}".format(ReadPDU(241, 67, 2)[1])
# PDU.Tpower8 = int(Tpower8) / 10
# Telectrica8 = "{:0x}".format(ReadPDU(241, 69, 3)[0]) + "{:0x}".format(ReadPDU(241, 69, 3)[1]) + "{:0x}".format(
#     ReadPDU(241, 69, 3)[2])
# PDU.Telectrical8 = int(Telectrica8) / 1000

# # 温湿度报警标记
# HTalarm = "{:0X}".format(ReadPDU(241, 130, 1)[0])
# HTalarm1 = int(HTalarm[:2])  # 高八位
# HTalarm2 = int(HTalarm[-2:])  # 低八位
# if HTalarm1 == 10:
#     if HTalarm2 == 10:
#         PDU.HTalarm = "此时温度低于下限，湿度低于下限"
#     elif HTalarm2 == 11:
#         PDU.HTalarm = "此时温度低于下限，湿度高于上限"
# if HTalarm == 11:
#     if HTalarm2 == 10:
#         PDU.HTalarm = "此时温度高于上限，湿度低于下限"
#     if HTalarm2 == 11:
#         PDU.HTalarm = "此时温度高于上限，湿度高于上限"
# else:
#     PDU.HTalarm = "温度湿度一切正常"

# # 欠压阀值
# Undervoltage = "{:0X}".format(ReadPDU(241, 131, 1)[0])
# if 0 < int(Undervoltage) / 10 < 255:
#     PDU.Undervoltage = str(int(Undervoltage) / 10) + "V"
# # 过压阀值
# Overvoltage = "{:0X}".format(ReadPDU(241, 132, 1)[0])
# if 0 < int(Overvoltage) / 10 < 255:
#     PDU.Overvoltage = str(int(Overvoltage) / 10) + "V"
#
# # 总过流报警阀值
# Tovercurrent = "{:0X}".format(ReadPDU(241, 133, 1)[0])
# PDU.Tovercurrent = str(int(Tovercurrent) / 100) + "A"
#
# # 支路过流报警阀值
# Boverflow = "{:0X}".format(ReadPDU(241, 134, 1)[0])
# PDU.Boverflow = str(int(Boverflow) / 100) + "A"
#
# # 总有功功率告警阈值
# TPthoreshold = "{:0X}".format(ReadPDU(241, 135, 1)[0])
# if 0 < int(TPthoreshold) / 100 < 99.99:
#     PDU.TPthreshold = str(int(TPthoreshold) / 100) + "KW"
#
# # 支路功率告警阀值
# Bpthreshold = "{:0X}".format(ReadPDU(241, 136, 1)[0])
# if 0 < int(Bpthreshold) / 100 < 99.99:
#     PDU.Bpthreshold = str(int(Bpthreshold) / 100) + "KW"
#
# # 温度上限
# Utlimit = "{:0X}".format(ReadPDU(241, 137, 1)[0])
# if 0 < int(Utlimit) / 100 < 99.99:
#     PDU.Utlimit = str(int(Utlimit) / 100) + "\u2103"
# # 温度下限
# Ltlimit = "{:0X}".format(ReadPDU(241, 138, 1)[0])
# if 0 < int(Ltlimit) / 100 < 99.99:
#     PDU.Ltlimit = str(int(Ltlimit) / 100) + "\u2103"
#
# # 湿度上限
# Uhlimit = "{:0X}".format(ReadPDU(241, 139, 1)[0])
# sever.execute(241, 5, 139, output_value=9000)
# if 0 < int(Uhlimit) / 100 < 99.99:
#     PDU.Uhlimit = str(int(Uhlimit) / 100) + "%Rh"
# # 湿度下限
# Lhlimit = "{:0X}".format(ReadPDU(241, 140, 1)[0])
# if 0 < int(Lhlimit) / 100 < 99.99:
#     PDU.Lhlimit = str(int(Lhlimit) / 100) + "%Rh"

# # 烟感传感器告警记录
# Smoke = "{:0X}".format(ReadPDU(241, 147, 3)[0])
# Smoke1 = "{:0X}".format(ReadPDU(241, 147, 3)[1])
# Smoke2 = "{:0X}".format(ReadPDU(241, 147, 3)[2])
# if str(Smoke2[-2:]) == '00':
#     PDU.Smoke = "烟感报警器无触发动作"
# if str(Smoke2[-2:]) == '0E':
#     PDU.Smoke = str(Smoke[:2]) + "月" + str(Smoke[-2:]) + "日" + str(Smoke1[:2]) + "点" + str(Smoke1[-2:]) + "分" + str(
#         Smoke2[:2]) + "秒" + "烟感报警器触发"
#
# # 水浸传感器告警记录
# water = "{:0X}".format(ReadPDU(241, 150, 3)[0])
# water1 = "{:0X}".format(ReadPDU(241, 150, 3)[1])
# water2 = "{:0X}".format(ReadPDU(241, 150, 3)[2])
# if str(water2[-2:]) == '00':
#     PDU.water = "水浸报警器无触发动作"
# if str(water2[-2:]) == '0E':
#     PDU.water = str(water[:2]) + "月" + str(water[-2:]) + "日" + str(water1[:2]) + "点" + str(water1[-2:]) + "分" + str(
#         water2[:2]) + "秒" + "水浸报警器触发"
#
# # 防雷计数器告警记录，防雷计数器告警次数
# Plightning = "{:0X}".format(ReadPDU(241, 153, 3)[0])
# Plightning1 = "{:0X}".format(ReadPDU(241, 153, 3)[1])
# Plightning2 = "{:0X}".format(ReadPDU(241, 153, 3)[2])
# Plfrequency = "{:0X}".format(ReadPDU(241, 156, 1)[0])
# if str(Plightning2[-2:]) == '00':
#     PDU.Plightning = "防雷计数器无触发动作"
#     if 0 < int(Plfrequency) < 9999:
#         PDU.Plfrequency = str(int(Plfrequency)) + "次"
# if str(Plightning2[-2:]) == '0E':
#     PDU.Plightning = str(int(Plightning[:2])) + "月" + str(int(Plightning[-2:])) + "日" + str(
#         int(Plightning1[:2])) + "点" + str(
#         int(Plightning1[-2:])) + "分" + str(int(Plightning2[:2])) + "秒" + "防雷计数器触发"
#     if 0 < int(Plfrequency) < 9999:
#         PDU.Plfrequency = str(int(Plfrequency)) + "次"
if __name__ == '__main__':
    mqtt_publish()
