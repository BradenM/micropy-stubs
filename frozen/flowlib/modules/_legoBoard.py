from micropython import const
import uos as os
import utime as time
import machine
import ustruct
import math
import i2c_bus
from pid import PID
import module

PORT1 = const(1)
PORT2 = const(2)
PORT3 = const(3)
PORT4 = const(4)

_MAX_INCR = 35
_MAX_THRESHOLD = 35
_MOTOR_DEAD_ZONE = 20

LEGO_BOARD_I2C_ADDR = const(0x56)
MOTOR_CTRL_ADDR = const(0x00)
MOTOR_CTRL_LEN = const(2)
ENCODER_READ_ADDR = const(0x08)
ENCODER_READ_LEN = const(4)


def constrain(amt, low, high):
    if amt < low:
        return low
    if amt > high:
        return high
    return amt


class NXP_Motor:
    def __init__(self, port):
        self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        
        self._available()

        self.port = port - 1
        self.prev_enc_val = 0
        self.interval = 0
        self.sample_interval = 10

        self.enc_zero = 0
        self.input_value = 0

        self.speed_pid = PID(p=50, i=0, d=60)
        self.speed_point = None

        self.angle_pid = PID(p=8, i=0, d=30)
        self.angle_point = None
        self.angle_max_pwm = 255

        self.encode_zero = 0
        self.encode_clear()
    
    def _available(self):
        if self.i2c.is_ready(LEGO_BOARD_I2C_ADDR) or self.i2c.is_ready(LEGO_BOARD_I2C_ADDR):
            pass
        else:
            raise module.Module("Lego module maybe not connect")

    def reset(self):
        self.stop()
        self.encoder_incr()

    def stop(self):
        self.set_pwm(0)
        self.angle_point = None
        self.speed_point = None

    def brake(self):
        # self.set_pwm(0)
        self.set_speed(0)

    def write(self, value):
        self.angle_point = None
        self.speed_point = None
        self.set_pwm(value)
    
    def read(self):
        return self.encoder_read()

    def encoder_incr(self):
        enc_val = self.encoder_read()
        incr_val = enc_val - self.prev_enc_val
        self.prev_enc_val = enc_val
        return incr_val

    def set_pwm(self, pwm):
        _pwm = constrain(pwm, -255, 255)
        buf = ustruct.pack('<h', int(_pwm))
        self.i2c.writeto_mem(
            LEGO_BOARD_I2C_ADDR, MOTOR_CTRL_ADDR + (self.port * MOTOR_CTRL_LEN), buf)

    def encoder_read(self):
        return self._encoder_read() - self.encode_zero

    def encode_clear(self):
        self.encode_zero = self._encoder_read()

    def _encoder_read(self):
        buf = bytearray(4)
        self.i2c.readfrom_mem_into(
            LEGO_BOARD_I2C_ADDR, ENCODER_READ_ADDR + (self.port * ENCODER_READ_LEN), buf)
        return (tuple(ustruct.unpack('<l', buf))[0])

    def set_speed(self, speed):
        # 0-27
        # self.speed_point = speed / (1000/self.sample_interval*60)
        self.angle_point = None
        self.speed_point = speed
        self.encoder_incr()

    def set_angle_zero(self):
        self.enc_zero = self.encoder_read()
        self.input_value = 0

    def set_angle(self, angle, max_pwm=255):
        self.speed_point = None
        self.angle_point = angle * 2
        self.angle_pid._min_output = -max_pwm
        self.angle_pid._max_output = max_pwm

    def update(self):
        if time.ticks_us() >= self.interval:
            self.interval = time.ticks_us() + 10000

            if not self.angle_point == None:
                self.input_value = self.encoder_read() - self.enc_zero
                output_value = self.angle_pid.get_pid(self.input_value, self.angle_point)
                self.set_pwm(output_value)

            if not self.speed_point == None:
                # Encoder filter
                self.input_value *= 0.75
                self.input_value += self.encoder_incr() * 0.25
                # self.input_value = constrain(self.input_value, -30, 30)
                # Output pwm
                output_value = self.speed_pid.get_pid(self.input_value, self.speed_point)
                self.set_pwm(output_value)
                # print("in:%0.2f, out:%0.2f\r\n" % (self.input_value, output_value))

    def update_no_block(self):
        if not self.angle_point == None:
            self.input_value = self.encoder_read() - self.enc_zero
            output_value = self.angle_pid.get_pid(self.input_value, self.angle_point)
            print(self.input_value - self.angle_point, end="\t")
            print(output_value)
            self.set_pwm(output_value)

        if not self.speed_point == None:
            # Encoder filter
            self.input_value *= 0.75
            self.input_value += self.encoder_incr() * 0.25
            # self.input_value = constrain(self.input_value, -30, 30)
            # Output pwm
            output_value = self.speed_pid.get_pid(self.input_value, self.speed_point)
            self.set_pwm(output_value)

    def test(self):
        while True:
            self.update()
        self.set_pwm(0)

    def deinit(self):
        pass

class Lego_Motor:
    def __init__(self):
        import _thread
        self.motor = {}
        _thread.start_new_thread('motor_update', self.update_thread, ())

    def update_thread(self):
        while True:
            time.sleep_ms(10)
            for i in self.motor.keys():
                self.motor[i].update_no_block()

    def register(self, number):
        self.motor[number] = LegoBoard(number)
        return self.motor[number]
    
    def unregistered(self, number):
        if number in self.motor.keys():
            self.motor.pop(number)
            return True
        else:
            return False

class LegoBoard:
    def __init__(self):
        self.M1 = NXP_Motor(1)
        self.M2 = NXP_Motor(2)
        self.M3 = NXP_Motor(3)
        self.M4 = NXP_Motor(4)
    
    def deinit(self):
        self.M1.deinit()
        self.M2.deinit()
        self.M3.deinit()
        self.M4.deinit()