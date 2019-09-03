import machine
controlMap =[
  [  4,  4,  5,  5,  6,  6,  7,  7,  7,  7, 7, 7, 7, 7, 7],
  [  2,  3,  4,  4,  5,  5,  6,  6,  6,  6, 6, 6, 6, 6, 7],
  [  0,  1,  3,  4,  4,  5,  5,  5,  5,  5, 5, 5, 5, 6, 7],
  [ -1,  0,  1,  2,  2,  3,  4,  4,  4,  4, 4, 4, 5, 6, 7],
  [ -2, -1,  0,  0,  2,  2,  3,  3,  3,  3, 3, 4, 5, 6, 7],
  [ -4, -3, -1, -1,  0,  1,  2,  2,  2,  2, 3, 4, 5, 6, 7],
  [ -6, -5, -3, -2, -1,  0,  0,  1,  1,  2, 3, 4, 5, 6, 7],
  [ -7, -6, -5, -4, -3, -2, -1,  0,  1,  2, 3, 4, 5, 6, 7],
  [ -7, -6, -5, -4, -3, -2,  0, -1, -1,  0, 1, 2, 3,  4, 5],
  [ -6, -5, -4, -3, -2, -1,  0, -2, -2, -2, -1, 0, 1, 2, 3],
  [ -6, -5, -4, -3, -2, -2, -3, -3, -3, -3, -3, -2, -1, 0, 1],
  [ -5, -4, -3, -2, -3, -3, -4, -4, -4, -4,  -4,  -4,  -3,  2, -1],
  [ -5, -4, -3, -3, -4, -4, -5, -5, -5, -5,  -5,  -5,  -5,  4, -3],
  [ -4, -3, -4, -4, -5, -5, -6, -6, -6, -6,  -6,  -6,  -6,  -6,  -5],
  [ -4, -4, -5, -5, -6, -6, -7, -7, -7, -7,  -7,  -7,  -7,  -7,  -7]
]

class LidarStep:
    def __init__(self):
        self.uart = machine.UART(2, baudrate=115200, tx=17, rx=-2)
    
    def setRgb(self, color_in, direction=None):
        data = bytearray(5)
        data[1], data[2], data[3] = color_in >> 16, (color_in & 0xffff) >> 8, color_in & 0xff
        data[4] = 0x55
        if direction == 'all' or direction == None:
            data[0] = 0xae
        elif direction == 'front':
            data[0] = 0xac
        elif direction == 'back':
            data[0] = 0xad
        self.uart.write(data)

    def setOneRgb(self, num, color_in):
        data = bytearray(6)
        data[0], data[5] = 0xab, 0x55
        data[1], data[2], data[3], data[4] = num, color_in >> 16, (color_in & 0xffff) >> 8, color_in & 0xff
        self.uart.write(data)

    def goAhead(self, speed):
        self.setStepMotor(speed, speed, speed, speed)

    def goBack(self, speed):
        self.setStepMotor(-speed, -speed, -speed, -speed)
    
    def turnLeft(self, speed):
        self.setStepMotor(-speed, speed, -speed, speed)
    
    def turnRight(self, speed):
        self.setStepMotor(speed, -speed, speed, -speed)

    def controlWheel(self, X, Y):
        spX = controlMap[-Y + 7][X + 7]
        spY = controlMap[-Y + 7][14 - X - 7]
        spZ = controlMap[-Y + 7][X + 7]
        spA = controlMap[-Y + 7][14 - X - 7]
        self.setStepMotor(spX, spY, spZ, spA)

    def setStepMotor(self, speedX, speedY, speedZ, speedA):
        data = bytearray(6)
        data[0], data[5] = 0xaa, 0x55
        data[1], data[2], data[3], data[4] = speedX, speedY, speedZ, speedA
        self.uart.write(data)

    def setServo(self, num, angle):
        data = bytearray(3)
        data[0] = 0xb0 if num else 0xaf
        data[1] = angle
        data[2] = 0x55
        self.uart.write(data)

        # self.uart.deinit()

class LidarBot(LidarStep):
    def __init__(self):
        import lidar
        lidar.init()
        LidarStep.__init__(self)
        self.lidar = lidar
    
    def deinit(self):
        self.lidar.deinit()
        try:
            self.uart.deinit()
        except:
            pass
