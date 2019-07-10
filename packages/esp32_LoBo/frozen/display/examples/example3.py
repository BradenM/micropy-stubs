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
gfx.fill_rect(0, 15, 128, 15, 1)
write15.text("micropython-oled", 0, 15, bgcolor=1, color=0)
for i in range(10):
    if i % 2:
        color, bgcolor = 1, 0
    else:
        color, bgcolor = 0, 1

    write20.text("{}".format(i), i * 10, 35, bgcolor=bgcolor, color=color)

gfx.rect(0, 35, 1 + (i + 1) * 10, 20, 1)
oled.show()
