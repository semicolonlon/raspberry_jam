import network
import socket
import time
from machine import ADC,Pin

server_ip = 'your_ip'
server_port = 5005

addr = (server_ip, server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

adc_x = ADC(26)
adc_y = ADC(27)
sw = Pin(16, Pin.IN, Pin.PULL_UP)

while True:
    if wlan.isconnected():
        axis_x = adc_x.read_u16()
        axis_y = adc_y.read_u16()
        msg = '{},{},{}'.format(axis_x, axis_y, sw.value())
        sock.sendto(msg.encode(), addr)
    else:
        print("Wi-Fi disconnected")
        led.value(0)
    time.sleep(0.01)
