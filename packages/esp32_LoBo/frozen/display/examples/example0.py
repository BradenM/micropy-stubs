from machine import Pin, I2C
import utime
from oled import SSD1306_I2C

scl = Pin(15)
sda = Pin(4)

i2c = I2C(scl=scl, sda=sda)
Pin(16, Pin.OUT, value=1)

oled = SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.text("Espresso IDE", 0, 1)
oled.text("micropython-oled", 0, 11)
oled.show()

utime.sleep(1)
for i in range(128):
    oled.scroll(-1, 0)
    oled.show()
    utime.sleep_ms(10)

oled.fill(0)
oled.text("Espresso IDE", 0, 1)
oled.text("micropython-oled", 0, 11)

for i in range(64):
    oled.scroll(0, 1)
    oled.show()
    utime.sleep_ms(10)
