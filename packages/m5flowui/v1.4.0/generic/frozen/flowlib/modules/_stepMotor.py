from utime import sleep_ms
import i2c_bus
import ure as re
import math
import module

class StepMotor:
  def __init__(self, addr = 0x70, i2c = None):
    if i2c == None:
      self.i2c = i2c_bus.get(i2c_bus.PORTA)
    else:
      self.i2c = i2c
    self.addr = addr
    self._available()
    self.mode = 'absolute' # absolute
    self.last_speed = 300

  def _available(self):
      if self.i2c.is_ready(self.addr) or self.i2c.is_ready(self.addr):
          pass
      else:
          raise module.Module("Module Step motor maybe not connect")

  # 1.6 = 360°
  def turn(self, x=0, y=0, z=0, speed = None):
    command = 'G1'
    command += ' X{}'.format(x) if x else ''
    command += ' Y{}'.format(y) if y else ''
    command += ' Z{}'.format(z) if z else ''
    command += ' F{}'.format(speed) if speed else ''
    self.last_speed = speed if speed else self.last_speed
    self.g_code(command)

  def g_code(self, code):
    self.i2c.writeto(self.addr, code + '\n')
    time = self.get_code_time(code)
    return time

  # 
  def set_mode(self, mode):
    if mode == 'distance':
      self.i2c.writeto(self.addr, 'G91\n')
      self.mode = mode 
    elif mode == 'absolute':
      self.i2c.writeto(self.addr, 'G90\n')
      self.mode = mode

  # get grbl run the g code used time 
  def get_code_time(self, g_code):
    x_value = re.search('X-*\d+', g_code)
    y_value = re.search('Y-*\d+', g_code)
    z_value = re.search('Z-*\d+', g_code)
    speed = re.search('F\d+', g_code)
    hold = re.search('P\d+', g_code)
    hold = float(hold.group(0)[1:])*1000 if hold else 0
    x_value = int(x_value.group(0)[1:]) if x_value else 0
    y_value = int(y_value.group(0)[1:]) if y_value else 0
    z_value = int(z_value.group(0)[1:]) if z_value else 0
    self.last_speed = int(speed.group(0)[1:]) if speed else self.last_speed
    time = math.sqrt(x_value*x_value + y_value*y_value + z_value*z_value) * 60 * 1000 / self.last_speed
    time += hold
    return int(time) 

  #  
  def grbl_init(self, x_step=None, y_step=None, z_step=None, acc=None):
    if x_step:
      self.i2c.writeto(self.addr, '$0={}\n'.format(x_step))
      sleep_ms(10)
    if y_step:
      self.i2c.writeto(self.addr, '$1={}\n'.format(y_step))
      sleep_ms(10)
    if z_step:
      self.i2c.writeto(self.addr, '$2={}\n'.format(z_step))
      sleep_ms(10)
    if acc:
      self.i2c.writeto(self.addr, '$8={}\n'.format(acc))

  # clean grbl return message
  def read_clean(self):
    while True:
      data = self.i2c.readfrom(self.addr, 1)
      if data == b'\x00':
        break

  # read grbl return message  
  def read_line(self):
    i2c_data = ''
    while True:
      data = self.i2c.readfrom(self.addr, 1)
      if data == b'\x00' or data == b'\n':
        break
      i2c_data += data.decode()
    return i2c_data[:-1]

  # read grbl state
  def read_idle(self):
    self.read_clean()
    self.i2c.writeto(self.addr, '@')
    state = self.i2c.readfrom(self.addr, 1)
    return state.decode() == 'I'

  # wait grbl idle 
  def wait_idle(self):
    self.read_clean()
    while True:
      self.i2c.writeto(self.addr, '@')
      state = self.i2c.readfrom(self.addr, 1)
      if state == b'I':
        break
      sleep_ms(5)
  
  # set motor always enable
  def lock_motor(self):
    self.g_code('$7=255')

  # restore motor enable status
  def unlock_motor(self):
    self.g_code('$7=25')
  
  def deinit(self):
    pass