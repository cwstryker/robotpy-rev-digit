import wpilib

I2C_DEV_ADDR = 0x70
BUTTON_A_PORT = 19
BUTTON_B_PORT = 20
POT_PORT = 3


class RevDigitBoard:
    def __init__(self):
        self._i2c = wpilib.I2C(wpilib.I2C.Port.kMXP, I2C_DEV_ADDR)
        self._button_a = wpilib.DigitalInput(BUTTON_A_PORT)
        self._button_b = wpilib.DigitalInput(BUTTON_B_PORT)
        self._potentiometer = wpilib.AnalogInput(POT_PORT)
        self._init_display()

    @property
    def button_a(self) -> bool:
        return self._button_a.getValue()

    @property
    def button_b(self) -> bool:
        return self._button_b.getValue()

    @property
    def potentiometer(self) -> float:
        return self._potentiometer.getVoltage()

    def write_display(self, message: str | float) -> None:
        pass

    def clear_display(self) -> None:
        self._write_display(b"\x00\x00\x00\x00\x00\x00\x00\x00")

    def _write_display(self, data: bytes) -> None:
        buffer = b"\x0F\x0F" + data
        self._i2c.writeBulk(buffer)

    def _init_display(self):
        """Initialize the display"""
        self._i2c.writeBulk(b"\x21")  # Enable display oscillator
        self._i2c.writeBulk(b"\xEF")  # Set to full brightness
        self._i2c.writeBulk(b"\x81")  # Turn on display, no blinking
        self.clear_display()
