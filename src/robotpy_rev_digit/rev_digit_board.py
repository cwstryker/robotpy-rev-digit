import wpilib

I2C_DEV_ADDR = 0x70
BUTTON_A_PORT = 19
BUTTON_B_PORT = 20
POT_PORT = 3

#  Display digit bit positions
#     ---- 8 ----
#   |  \   |   /  |
#   13  0  1  2   9
#   |    \ | /    |
#    -14-     -15-
#   |    / | \    |
#   12  5  4  3   10
#   |  /   |   \  |
#     ---  11 ---    .6


CHAR_MAP = {
    "0": b"\x3F\x00",
    "1": b"\x06\x00",
    "2": b"\xDB\x00",
    "3": b"\xCF\x00",
    "4": b"\xE6\x00",
    "5": b"\xED\x00",
    "6": b"\xFD\x00",
    "7": b"\x07\x00",
    "8": b"\xFF\x00",
    "9": b"\xEF\x00",
    "0.": b"\x3F\x40",
    "1.": b"\x06\x40",
    "2.": b"\xDB\x40",
    "3.": b"\xCF\x40",
    "4.": b"\xE6\x40",
    "5.": b"\xED\x40",
    "6.": b"\xFD\x40",
    "7.": b"\x03\x40",
    "8.": b"\xFF\x40",
    "9.": b"\xEF\x40",
    "A": b"\xF7\x00",
    "B": b"\x8F\x12",
    "C": b"\x39\x00",
    "D": b"\x0F\x12",
    " ": b"\x00\x00",
}


def format_float(number: float) -> str:
    """Convert a float into a string with four digits max and one decimal digit"""
    rounded = round(number, 1)  # round the number to one decimal digit
    if (rounded > 999.9) or (rounded < -99.9):
        result = "####"  # Cannot display such an extreme number
    else:
        result = f"{number:5.1f}"[:5]
    return result


def format_string(message: str) -> str:
    """Align and pad the message to the given length."""
    return f"{str(message)[:4]:>4}"


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

    def _display_float(self, message: float) -> None:
        buf = b""
        for i, c in enumerate(format_float(message)):
            # lookup the decimal point version of the third digit
            if i == 2:
                c += "."
            # ignore the decimal point character
            elif i == 3:
                continue
            # translate the character into the byte code
            try:
                buf = CHAR_MAP[c] + buf
            except KeyError:
                buf = b"\xFF\xFF" + buf  # Unsupported characters are left blank
        self._write_display(buf)

    def _display_string(self, message: str) -> None:
        buf = b""
        for c in format_string(message):
            try:
                buf = CHAR_MAP[c] + buf
            except KeyError:
                buf = b"\xFF\xFF" + buf  # Unsupported characters are left blank
        self._write_display(buf)

    def display_message(self, message: str | float) -> None:
        if isinstance(message, float):
            self._display_float(message)
        else:
            self._display_string(message)

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
