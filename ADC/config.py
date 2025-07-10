import time
import spidev
import RPi.GPIO

GPIO = RPi.GPIO
SPI = spidev.SpiDev(0, 0)

RST_PIN     = 18
CS_PIN      = 22
DRDY_PIN    = 17


def digital_write(self, pin, value):
    GPIO.output(pin, value)

def digital_read(self, pin):
    return GPIO.input(pin)

def delay_ms(self, delaytime):
    time.sleep(delaytime / 1000.0)

def spi_writebyte(self, data):
    SPI.writebytes(data)

def spi_readbytes(self, reg):
    return SPI.readbytes(reg)

def module_init(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RST_PIN, GPIO.OUT)
    GPIO.setup(CS_PIN, GPIO.OUT)

    GPIO.setup(DRDY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    SPI.max_speed_hz = 2000000
    SPI.mode = 0b01
    return 0

def module_exit(self):
    SPI.close()
    GPIO.output(RST_PIN, 0)
    GPIO.output(CS_PIN, 0)
    GPIO.cleanup()