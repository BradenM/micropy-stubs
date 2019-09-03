from micropython import const
import uos as os
import utime as time
import machine
import ustruct
from mpu6050 import MPU6050
import i2c_bus

M5GO_WHEEL_ADDR = const(0x56)
MOTOR_CTRL_ADDR = const(0x00)
ENCODER_ADDR = const(0x04)


#define constrain(amt,low,high) (amt)<(low)?(low):((amt)>(high)?(high):(amt))
def constrain(amt, low, high):
    if amt < low:
        return low
    if amt > high:
        return high
    return amt


class M5bala:
    def __init__(self, i2c=None):
        if i2c is None:
            self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        else:
            self.i2c = i2c
        self.imu = MPU6050(self.i2c)

        if self.i2c.is_ready(M5GO_WHEEL_ADDR) or self.i2c.is_ready(M5GO_WHEEL_ADDR):
            pass
        else:
            raise ImportError("Bala Motor not connect")

        self.id = self.imu.whoami
        # self.set_motor(0, 0)
        self.imu.setGyroOffsets(-2.71, -0.01, -0.04)
        self.loop_interval = time.ticks_us()
        self.dt = time.ticks_us()
        self.angleX = 0
        self.angleX_offset = 0
        self.last_angle = 0.0
        self.last_wheel = 0.0
        self.in_speed0 = 0
        self.in_speed1 = 0
        self.left = 0
        self.right = 0
        self.K1 = 40
        self.K2 = 40
        self.K3 = 6.5
        self.K4 = 5.5
        self.K5 = 0
        self.enc_filter = 0.90

    def stop(self):
        self.left = 0
        self.right = 0
        
    def move(self, speed, duration=5):
        self.left = -speed
        self.right = -speed
        # time.sleep(duration)
        # self.stop()

    def turn(self, speed, duration=5):
        if speed > 0: # Turn RIGHT
            self.left = abs(speed)
            self.right = 0
        elif speed < 0: # Turn LEFT
            self.left = 0
            self.right = abs(speed)
        # time.sleep(duration)
        # self.stop()
    
    def rotate(self, speed, duration=2):
        if speed > 0:
            self.left = speed
            self.right = -speed
        elif speed < 0:
            self.left = speed
            self.right = -speed
        # time.sleep(duration)
        # self.stop()

    def set_motor(self, m0_pwm, m1_pwm):
        buf = ustruct.pack('<hh', int(m0_pwm), int(m1_pwm))
        try:
            self.i2c.writeto_mem(M5GO_WHEEL_ADDR, MOTOR_CTRL_ADDR, buf)
        except:
            pass

    def read_encoder(self):
        buf = bytearray(4)
        return_value = [0, 0]
        try:
            self.i2c.readfrom_mem_into(M5GO_WHEEL_ADDR, ENCODER_ADDR, buf)
            return_value =  tuple(ustruct.unpack('<hh', buf))
        except:
            pass
        return return_value
        
    def balance(self):
        if time.ticks_us() >= self.loop_interval: # 10ms
            self.loop_interval = time.ticks_us() + 10000

            # Angle X sample
            pitch = self.imu.ypr[1]
            if self.id == 0x71:
                pitch = -pitch
            self.angleX = (pitch + self.angleX_offset)

            # Car Down
            if self.angleX > 45 or self.angleX < -45:
                self.set_motor(0, 0)
                return

            # Encoder sample
            new_speed0, new_speed1 = self.read_encoder()
            self.in_speed0 *= self.enc_filter
            self.in_speed0 += -new_speed0 * (1 - self.enc_filter)
            self.in_speed1 *= self.enc_filter
            self.in_speed1 += new_speed1 * (1 - self.enc_filter)

            # ========== PID computing ==========
            # -- Angle
            angle = self.angleX
            angle_velocity = angle - self.last_angle
            self.last_angle = angle

            # -- Postiton
            wheel = int(self.in_speed0 + self.in_speed1) // 2
            wheel_velocity = wheel - self.last_wheel
            self.last_wheel = wheel

            # -- PID
            torque = (angle_velocity * self.K1) + (angle * self.K2) + (wheel_velocity * self.K3) + (wheel * self.K4)
            torque = constrain(torque, -255, 255)
            
            # -- Wheel offset
            speed_diff = 0
            # speed_diff = (int(self.in_speed0) - int(self.in_speed1))
            # speed_diff *= self.K5

            # -- PWM OUT
            self.set_motor(torque + self.left - speed_diff, torque + self.right)


    def run(self, blocking=False):
        if blocking:
            while True:
                self.balance()
        else:
            self.balance()

    def start(self, thread=True):
        if thread:
            import _thread
            _thread.start_new_thread("m5bala", self.run, (True, ))
