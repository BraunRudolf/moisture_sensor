import machine
import utime

led = machine.Pin("LED", machine.Pin.OUT)

def blink_per_sec(time:int)->None:
    """
    Let's led blink once a second to indicate an on going process
    """
    sec = 0
    while sec < time:
        led.on()
        utime.sleep(0.5)
        led.off()
        utime.sleep(0.5)
        sec+=1


def shine_till_end(time:int)->None:
    """
    Let's the led shine for a given time to indicate time to perform
    an action
    """
    led.on()
    utime.sleep(time)
    led.off()
