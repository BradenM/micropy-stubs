from machine import Pin, I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20

scl = Pin(15)
sda = Pin(4)

i2c = I2C(scl=scl, sda=sda)
Pin(16, Pin.OUT, value=1)

oled = SSD1306_I2C(128, 64, i2c)

gfx = GFX(128, 64, oled.pixel)

gfx.rect(5, 5, 10, 15, 1)
gfx.fill_rect(20, 5, 10, 15, 1)

gfx.circle(50, 15, 10, 1)
gfx.fill_circle(75, 15, 10, 1)

gfx.triangle(50, 40, 10, 50, 15, 25, 1)
gfx.fill_triangle(50 + 70, 40, 10 + 70, 50, 15 + 70, 25, 1)

oled.show()


