# locomotion.py
"""
Motion Service - Locomotion control for Robot OS.
Handles all motor control and movement operations.
"""

from time import sleep
from config import logger, GPIO_CONFIG

try:
    from gpiozero import Motor
except ImportError:
    Motor = None


class MockMotor:
    """Fallback motor backend used for virtual machine simulation."""

    def __init__(self, name):
        self.name = name

    def forward(self, speed=0.0):
        logger.info("[SIM] %s forward at %s", self.name, speed)

    def backward(self, speed=0.0):
        logger.info("[SIM] %s backward at %s", self.name, speed)

    def stop(self):
        logger.info("[SIM] %s stop", self.name)

class RobotChassis:
    """
    Robot chassis controller for motion control.
    Manages left and right motor control for movement and steering.
    """
    
    def __init__(self, simulation=False):
        """Initialize the robot chassis with configured GPIO pins."""
        try:
            self.simulation = simulation or Motor is None

            if self.simulation:
                self.left_motors = MockMotor("left_motor")
                self.right_motors = MockMotor("right_motor")
                logger.info("Robot Chassis initialized in simulation mode")
                print("Simulation: Robot Chassis Initialized.")
                return

            # Initialize Left Motors using configured pins
            left_config = GPIO_CONFIG["LEFT_MOTOR"]
            self.left_motors = Motor(
                forward=left_config["forward"],
                backward=left_config["backward"],
                enable=left_config["enable"]
            )

            # Initialize Right Motors using configured pins
            right_config = GPIO_CONFIG["RIGHT_MOTOR"]
            self.right_motors = Motor(
                forward=right_config["forward"],
                backward=right_config["backward"],
                enable=right_config["enable"]
            )

            logger.info("✓ Robot Chassis initialized successfully")
            print("Hardware: Robot Chassis Initialized.")
        
        except Exception as e:
            logger.error(f"Error initializing RobotChassis: {e}")
            raise

    def move_forward(self, speed=0.8):
        """
        Moves the robot forward.
        
        Args:
            speed: Movement speed as float between 0.0 and 1.0
        """
        try:
            self.left_motors.forward(speed)
            self.right_motors.forward(speed)
            logger.debug(f"Moving forward at {speed*100}% speed")
            print(f"Moving Forward at {speed*100}% speed")
        except Exception as e:
            logger.error(f"Error moving forward: {e}")
            self.stop()

    def move_backward(self, speed=0.8):
        """
        Moves the robot backward.
        
        Args:
            speed: Movement speed as float between 0.0 and 1.0
        """
        try:
            self.left_motors.backward(speed)
            self.right_motors.backward(speed)
            logger.debug(f"Moving backward at {speed*100}% speed")
            print("Moving Backward")
        except Exception as e:
            logger.error(f"Error moving backward: {e}")
            self.stop()

    def turn_left(self, speed=0.6):
        """
        Tank steering: Left wheels go backward, right wheels go forward.
        
        Args:
            speed: Turn speed as float between 0.0 and 1.0
        """
        try:
            self.left_motors.backward(speed)
            self.right_motors.forward(speed)
            logger.debug(f"Turning left at {speed*100}% speed")
            print("Turning Left")
        except Exception as e:
            logger.error(f"Error turning left: {e}")
            self.stop()

    def turn_right(self, speed=0.6):
        """
        Tank steering: Left wheels go forward, right wheels go backward.
        
        Args:
            speed: Turn speed as float between 0.0 and 1.0
        """
        try:
            self.left_motors.forward(speed)
            self.right_motors.backward(speed)
            logger.debug(f"Turning right at {speed*100}% speed")
            print("Turning Right")
        except Exception as e:
            logger.error(f"Error turning right: {e}")
            self.stop()

    def stop(self):
        """Cuts power to all motors immediately."""
        try:
            self.left_motors.stop()
            self.right_motors.stop()
            logger.debug("Robot stopped")
            print("Robot Stopped")
        except Exception as e:
            logger.error(f"Error stopping robot: {e}")


# --- Quick Test Block ---
# If you run *only* this file, it will test the motors.
# If you import this file into main.py, this test won't run automatically.
if __name__ == "__main__":
    chassis = RobotChassis()
    chassis.move_forward(speed=0.5)  # Half speed
    sleep(2)                         # Move for 2 seconds
    chassis.stop()