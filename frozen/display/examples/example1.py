from machine import Pin, I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20

scl = Pin(15)
sda = Pin(4)

i2c = I2C(scl=scl, sda=sda)
Pin(16, Pin.OUT, value=1)

oled = SSD1306_I2C(128, 64, i2c)
gfx = GFX(128, 64, oled.pixel)

write15 = Write(oled, ubuntu_mono_15)
write20 = Write(oled, ubuntu_mono_20)

write15.text("Espresso IDE", 0, 0)
write15.text("micropython-oled", 0, 15)

gfx.line(0, 32, 127, 32, 1)
gfx.line(0, 33, 127, 33, 1)

write20.text("1234567890", 0, 35)
write15.text("Ubuntu Mono font", 0, 52)

oled.show()
