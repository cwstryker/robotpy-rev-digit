import wpilib

from robotpy_rev_digit import RevDigitBoard

I2C_DEV_ADDR = 0x70


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        # self.i2c = wpilib.I2C(wpilib.I2C.Port.kMXP, I2C_DEV_ADDR)
        self.display = RevDigitBoard()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self):
        """This function is called periodically during operator control."""
        buf = bytearray(
            [
                0x0F,
                0x0F,
                0x00,
                0x00,
                0x00,
                0x00,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
            ]
        )
        self.display._i2c.writeBulk(buf)


if __name__ == "__main__":
    wpilib.run(MyRobot)
