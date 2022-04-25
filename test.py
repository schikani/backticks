from machine import Pin, TouchPad
import time

led = Pin(2, Pin.OUT)
touch1 = TouchPad(Pin(14))
touch2 = TouchPad(Pin(12))
touch3 = TouchPad(Pin(13))


while True:
    try:
        # if touch.read() < 180:
        #     led.value(True)
        # else:
        #     led.value(False)
        print("WHITE: {} | BLUE: {} | PURPLE: {}"
        .format(touch1.read(), touch2.read(), touch3.read()))

        time.sleep_ms(500)

    except KeyboardInterrupt:
        break