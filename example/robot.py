import wpilib

from robotpy_rev_digit import RevDigitBoard

I2C_DEV_ADDR = 0x70

CHAR_MAP = {"A": b"\xF7\x00", "B": b"\x8F\x12", "C": b"\x39\x00", "D": b"\x0F\x12"}


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.display = RevDigitBoard()
        self.timer = wpilib.Timer()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self):
        """This function is called periodically during operator control."""
        self.timer.start()

    def teleopPeriodic(self):
        """This function is called periodically during autonomous."""
        self.display.display_message(self.timer.get())

    def teleopExit(self):
        """This function is called when teleop ends."""
        self.timer.stop()


if __name__ == "__main__":
    wpilib.run(MyRobot)
