import network
import socket
import time
from machine import ADC,Pin

server_ip = 'your ip'

addr = (server_ip, 5005)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

adc_x = ADC(26)
adc_y = ADC(27)
sw = Pin(16, Pin.IN, Pin.PULL_UP)

while True:
    if wlan.isconnected():
        axis_x = adc_x.read_u16()
        axis_y = adc_y.read_u16()
        msg = str(axis_x) + ',' + str(axis_y) + ',' +  str(sw.value())
        sock.sendto(msg.encode(), addr)
    time.sleep(0.1)

