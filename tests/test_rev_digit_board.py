from robotpy_rev_digit.rev_digit_board import RevDigitBoard
import wpilib
from wpilib.simulation import DIOSim, AnalogInputSim
import pytest


class I2CSim:
    def __init__(self, i2c_obj: wpilib.I2C):
        self._buffer = []
        self._i2c_obj = i2c_obj

    def writeBulk(self, array: bytearray):
        self._buffer.append(array)

    @property
    def buffer(self) -> list[bytearray]:
        return self._buffer


def test_RevDigit_Instance():
    """Test that a RevDigit object can be created"""
    digit = RevDigitBoard()
    assert isinstance(digit, RevDigitBoard)
    assert isinstance(digit._i2c, wpilib.I2C)
    assert isinstance(digit._button_a, wpilib.DigitalInput)
    assert isinstance(digit._button_b, wpilib.DigitalInput)
    assert isinstance(digit._potentiometer, wpilib.AnalogInput)


@pytest.mark.parametrize("state", [True, False])
def test_RevDigit_button_a(state):
    """Test reading the state of Button A"""
    digit = RevDigitBoard()
    digit._button_a = DIOSim(input=digit._button_a)
    digit._button_b = DIOSim(input=digit._button_b)
    digit._button_a.setValue(state)
    digit._button_b.setValue(not state)
    assert digit.button_a is state


@pytest.mark.parametrize("state", [True, False])
def test_RevDigit_button_b(state):
    """Test reading the state of Button B"""
    digit = RevDigitBoard()
    digit._button_a = DIOSim(input=digit._button_a)
    digit._button_b = DIOSim(input=digit._button_b)
    digit._button_a.setValue(not state)
    digit._button_b.setValue(state)
    assert digit.button_b is state


@pytest.mark.parametrize("voltage", [0.0, 1.0, 3.3, 5.0])
def test_RevDigit_potentiometer(voltage):
    """Test reading the state of the potentiometer sensor"""
    digit = RevDigitBoard()
    digit._potentiometer = AnalogInputSim(analogInput=digit._potentiometer)
    digit._potentiometer.setVoltage(voltage)
    assert digit.potentiometer == voltage


def test_RevDigit_clear_display():
    """Test that display can be cleared"""
    digit = RevDigitBoard()
    digit._i2c = I2CSim(i2c_obj=digit._i2c)  # Use a simulated I2C interface
    digit.clear_display()
    expected_packets = [b"\x0F\x0F\x00\x00\x00\x00\x00\x00\x00\x00"]
    for actual, expected in zip(digit._i2c.buffer, expected_packets):
        assert actual == expected


def test_RevDigit_display_init():
    """Test initializing the display"""
    digit = RevDigitBoard()
    digit._i2c = I2CSim(i2c_obj=digit._i2c)  # Use a simulated I2C interface
    digit._init_display()
    expected_packets = [
        b"\x21",
        b"\xEF",
        b"\x81",
        b"\x0F\x0F\x00\x00\x00\x00\x00\x00\x00\x00",
    ]
    for actual, expected in zip(digit._i2c.buffer, expected_packets):
        assert actual == expected
