import Adafruit_BBIO.PWM as PWM
import time

print "Start"
#optionally, you can set the frequency as well as the polarity from their defaults:
PWM.start("P9_14", 20, 10, 1)

time.sleep(30)

print "Stop"
PWM.stop("P9_14")
PWM.cleanup()


print "exit"