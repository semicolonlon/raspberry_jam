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

SSID = 'ssid'
PASSWORD = 'pass'

SERVER_IP = 'ip'
SERVER_PORT = 'port'

RETRY_WAIT_SEC = 5

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

adc_x = AnalogIn(board.GP26)
adc_y = AnalogIn(board.GP27)
sw = DigitalInOut(board.GP16)
sw.pull = Pull.UP

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
        sw_value = 0 if sw.value else 1

        msg = f"{axis_x},{axis_y},{sw_value}"
        sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))

        time.sleep(0.02)

    except OSError:
        if 'sock' in locals() and sock:
            sock.close()
        led.value = False
    except Exception:
        time.sleep(1)

