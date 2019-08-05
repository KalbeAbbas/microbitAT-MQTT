import time
from microbit import *
import ustruct as struct
import random


_WIFI_SSID = "" #Enter your Wi-Fi SSID
_WIFI_PASSWORD = "" #Enter your Wi-Fi Password
_USERNAME = "" #Enter your username/token
_PASSWORD = "" #Enter your password

uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin0)


def main():

    EspConnect("io.adafruit.com",1883)
    MQTTConnect()
    
    time.sleep(2)
	
    while True:
        num=random.randint(1,100)
        MQTTPublish(str(num))
        time.sleep(1)



def EspConnect(url,port):

    uart.write(bytearray("AT+CWMODE=1\r\n"))

    time.sleep(1)

    uart.write(bytearray("AT+CWJAP=\""+_WIFI_SSID+"\",\""+_WIFI_PASSWORD+"\"\r\n"))

    time.sleep(5)

    uart.write(bytearray("AT+CIPMODE=0\r\n"))

    time.sleep(1)

    uart.write(bytearray("AT+CIPSTART=\"TCP\",\""+url+"\","+str(port)+"\r\n"))

    time.sleep(1)


def MQTTConnect():

    protocol_name = bytearray(b"\x00\x04MQTT")

    protocol_lvl = bytearray(b"\x04")

    user_name_flag_bit = (1<<7)

    password_flag_bit  = (1<<6)

    clean_session_bit  = (1<<1)

    connect_flags_byte = user_name_flag_bit| password_flag_bit| clean_session_bit

    connect_flags = struct.pack("!B",connect_flags_byte)

    keep_alive = struct.pack("!H",200)

    client_id = bytearray(b"thermostat_controller")

    client_id_len = struct.pack("!H",len(client_id))

    username = bytearray(_USERNAME)

    username_len = struct.pack("!H",len(username))

    password = bytearray(_PASSWORD)

    password_len = struct.pack("!H",len(password))

    msg_part_two = protocol_name+ protocol_lvl+ connect_flags+ keep_alive+ client_id_len + client_id+ username_len + username+ password_len + password

    msg_part_one = struct.pack("!B",1<<4) + struct.pack("!B",len(msg_part_two))
	
    msg=msg_part_one+msg_part_two
	
    uart.write(bytearray("AT+CIPSEND=%d\r\n"%len(msg)))
	
    time.sleep(1)
	
    uart.write(msg)


def MQTTPublish(val):
    topic = b"KalbeAbbas/feeds/hellotest"

    topic_len = struct.pack("!H",len(topic))

    msg_part_two = topic_len+topic+bytearray(val)

    msg_part_one = struct.pack("!B",0x30) + struct.pack("!B",len(msg_part_two))
	
    msg=msg_part_one+msg_part_two

    uart.write("AT+CIPSEND=%d\r\n"%len(msg))
	
    time.sleep(1)
	
    uart.write(msg_part_one + msg_part_two)

if __name__ == '__main__':
    main()
