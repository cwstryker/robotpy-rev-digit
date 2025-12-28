# RobotPy Rev Digit

[![RobotPy - 2024](https://img.shields.io/badge/RobotPy-2025-2ea44f)](https://github.com/robotpy)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

A RobotPy module for control of the REV Robotics Digit Board.
Ported from the Java repository: https://github.com/vampjaz/REVDigitBoard

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install robotpy-rev-digit
```

## Usage
See the example robot.py file for an example for how to use the module.

```python
import wpilib
from robotpy_rev_digit import RevDigitBoard

I2C_DEV_ADDR = 0x70
TEST_PATTERN = "   ABCDEFGHIJKLMNOPQRSTUVWXYZ*?@#   "


class MyRobot(wpilib.TimedRobot):
    """
    ##########################################################################
    RevDigitBoard Example Program
    This program is an example of how to use the RevDigitBoard class.
    """

    # noinspection PyAttributeOutsideInit
    def robotInit(self):
        """
        This function is called upon program startup and should be used for any
        initialization code.
        """
        # initialize the robot
        self.timer = wpilib.Timer()
        self.robot = wpilib.RobotController
        self.rev_digit = RevDigitBoard()

    def robotPeriodic(self):
        """This function is called periodically regardless of the robot's state"""
        self.rev_digit.update()

    def teleopInit(self):
        """This function is run once each time the robot enters teleop mode."""
        self.timer.start()

    def teleopPeriodic(self):
        """This function is called periodically during teleop mode."""
        time = self.timer.get()
        idx = int(time // 1) % len(TEST_PATTERN)
        text = TEST_PATTERN[idx:]
        voltage = self.rev_digit.potentiometer_voltage

        # If neither button is pressed, show the timer
        if (not self.rev_digit.is_button_a_pressed) and (
            not self.rev_digit.is_button_b_pressed
        ):
            self.rev_digit.display_message(time)

        # If Button A is pressed, display the battery voltage
        elif self.rev_digit.is_button_a_pressed:
            self.rev_digit.display_message(voltage)

        # If Button B is pressed, display the test pattern
        elif self.rev_digit.is_button_b_pressed:
            self.rev_digit.display_message(text)

    def teleopExit(self):
        """This function is called when teleop mode ends."""
        self.timer.stop()

    def disabledPeriodic(self):
        """This function is called periodically when the robot is disabled"""
        voltage = self.robot.getBatteryVoltage()
        self.rev_digit.display_message(voltage)
```

## License

`robotpy-rev-digit` is distributed under the terms of the [GPL-3.0-only](https://spdx.org/licenses/MIT.html) license.
