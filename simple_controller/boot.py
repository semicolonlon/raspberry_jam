import network
import socket
import time
from machine import ADC,Pin

ssid = 'your_ssid'
password = 'your_pass'
server_ip = 'your_ip'
server_port = 5005

led = Pin('LED',Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,password)

print('connecting to Wi-Fi...')

while not wlan.isconnected():
    led.toggle()
    time.sleep(0.5)
    
led.value(1)

print("Connected! IP:", wlan.ifconfig()[0])

