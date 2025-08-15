# license semicolonlon 2025
# thank you !

# ピンの接続について
# 26 -> x
# 27 -> y
# 16 -> スイッチ(ジョイコン)
# 0 -> スイッチ(外部)
# 1 -> スイッチ(外部)

import wifi
import socketpool
import time
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

SSID = 'HR01a-DC45C3'
PASSWORD = '864a9ac3c3'

SERVER_IP = '192.168.128.102'
SERVER_PORT = 5005

RETRY_WAIT_SEC = 5

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

adc_x = AnalogIn(board.GP26)
adc_y = AnalogIn(board.GP27)
button = DigitalInOut(board.GP16)
button.pull = Pull.UP

sw1 = DigitalInOut(board.GP0)
sw1.pull = Pull.UP
sw2 = DigitalInOut(board.GP1)
sw2.pull = Pull.UP

while True:
    if not wifi.radio.ipv4_address:
        while not wifi.radio.ipv4_address:
            try:
                led.value = not led.value
                wifi.radio.connect(SSID, PASSWORD)
            except (ConnectionError, Exception):
                time.sleep(RETRY_WAIT_SEC)

        led.value = True
        pool = socketpool.SocketPool(wifi.radio)
        sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)

    try:
        axis_x = adc_x.value
        axis_y = adc_y.value
        button_value = 0 if button.value else 1
        sw1_value = 0 if sw1.value else 1
        sw2_value = 0 if sw2.value else 1

        msg = f"{axis_x},{axis_y},{button_value},{sw1_value},{sw2_value}"
        sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))

        time.sleep(0.02)

    except OSError:
        if 'sock' in locals() and sock:
            sock.close()
        led.value = False
    except Exception:
        time.sleep(1)
