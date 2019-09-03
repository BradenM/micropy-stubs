import unit
import machine
class Rgb_multi: 
    def __init__(self, port, number=143):
        self.port = port
        self.pin = port[0]
        self.number = number
        self.np = machine.Neopixel(self.pin, self.number)
        self.np.brightness(10)

    def setColor(self, num, color_in):
        self.np.set(num, color_in)

    def setColorFrom(self, begin, end, color_in):
        begin = min(self.number, max(begin, 1))
        end = min(self.number, max(end, 1))
        for i in range(begin, end+1):
            self.np.set(i, color_in, update=False)
        self.np.show()

    def setColorAll(self, color_in):
        for i in range(1, self.number+1):
            self.np.set(i, color_in, update=False)
        self.np.show()

    def setBrightness(self, brightness):
        brightness = min(255, max(0, brightness))
        self.np.brightness(brightness)
    
    def deinit(self):
        self.np.deinit()