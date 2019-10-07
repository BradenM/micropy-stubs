from machine import Pin, I2C
from oled import Write, SSD1306_I2C
import utime


class battery_status:
    _FONT = {
        'battery-empty': [20, 1099511627775, 1099511627775, 1099511627775, 824633720832, 824633720832, 17179869168, 17179869168, 68719476720, 68719476720, 17179869168, 17179869168, 824633720832, 824633720832, 1099511627775],
        'battery-quarter': [20, 1099511627775, 1099511627775, 1099511627775, 824633720832, 824633720832, 17179869168, 17179852848, 68719460400, 68719460400, 17179852848, 17179869168, 824633720832, 824633720832, 1099511627775],
        'battery-half': [20, 1099511627775, 1099511627775, 1099511627775, 824633720832, 824633720832, 17179869168, 17178820656, 68718428208, 68718428208, 17178820656, 17179869168, 824633720832, 824633720832, 1099511627775],
        'battery-three-quarters': [20, 1099511627775, 1099511627775, 1099511627775, 824633720832, 824633720832, 17179869168, 17112760368, 68652367920, 68652367920, 17112760368, 17179869168, 824633720832, 824633720832, 1099511627775],
        'battery-full': [20, 1099511627775, 1099511627775, 1099511627775, 824633720832, 824633720832, 17179869168, 12884901936, 64424509488, 64424509488, 12884901936, 17179869168, 824633720832, 824633720832, 1099511627775],
    }


scl = Pin(15)
sda = Pin(4)

i2c = I2C(scl=scl, sda=sda)
Pin(16, Pin.OUT, value=1)

oled = SSD1306_I2C(128, 64, i2c)
battery = Write(oled, battery_status)

oled.fill(0)
battery.char('battery-empty', 108, 0)
oled.show()
utime.sleep(0.5)

oled.fill(0)
battery.char('battery-quarter', 108, 0)
oled.show()
utime.sleep(0.5)

oled.fill(0)
battery.char('battery-half', 108, 0)
oled.show()
utime.sleep(0.5)

oled.fill(0)
battery.char('battery-three-quarters', 108, 0)
oled.show()
utime.sleep(0.5)

oled.fill(0)
battery.char('battery-full', 108, 0)
oled.show()
utime.sleep(0.5)