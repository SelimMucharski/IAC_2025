from ADS1263 import ADS1263

class ADC(ADS1263):
    def __init__(self, rst_pin, cs_pin, drdy_pin):
        super().__init__()
        self.rst_pin = rst_pin
        self.cs_pin = cs_pin
        self.drdy_pin = drdy_pin
