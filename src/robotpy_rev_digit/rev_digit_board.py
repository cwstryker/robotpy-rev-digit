import wpilib

I2C_DEV_ADDR = 0x70
BUTTON_A_PORT = 19
BUTTON_B_PORT = 20
POT_PORT = 3


class RevDigit:
    def __init__(self):
        self._i2c = wpilib.I2C(wpilib.I2C.Port.kMXP, I2C_DEV_ADDR)
        self._button_a = wpilib.DigitalInput(BUTTON_A_PORT)
        self._button_b = wpilib.DigitalInput(BUTTON_B_PORT)
        self._pot = wpilib.AnalogInput(POT_PORT)
