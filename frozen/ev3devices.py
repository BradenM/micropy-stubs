from pybricks.parameters import Button, Color, Direction, Port, Stop
from typing import List, Tuple


class Motor:
    """
    LEGO® MINDSTORMS® EV3 Medium or Large Motor. Element 99455/6148292 or 95658/6148278, contained in:
    - 31313: LEGO® MINDSTORMS® EV3 (2013)
    - 45544: LEGO® MINDSTORMS® Education EV3 Core Set (2013)
    - 45503 or 45502: Separate part (2013)
    """

    def __init__(self, port: Port, direction: Direction = Direction.CLOCKWISE, gears: List[int, int] = None):
        """
        LEGO® MINDSTORMS® EV3 Medium or Large Motor.
        ----------

        port : Port – Port to which the motor is connected.

        direction : Direction – Positive speed direction (Default: Direction.CLOCKWISE).

        gears : List[int, int] – List of gears linked to the motor (Default:None). For example: [12, 36] represents a gear train with a 12-tooth and a 36-tooth gear. Use a list of lists for multiple gear trains, such as [[12, 36], [20, 16, 40]]. The gears setting is only available for motors with rotation sensors.
        """
        ...

    def dc(self, duty: float):
        """
        Set the duty cycle of the motor.

        ----------
        duty : float - The duty cycle as a percentage (-100.0 to 100).
        """
        ...

    def angle(self) -> int:
        """
        Get the rotation angle of the motor.

        ----------
        Returns - Motor angle in degrees.
        """
        ...

    def reset_angle(self, angle: int):
        """
        Reset the accumulated rotation angle of the motor.

        ----------
        angle : float – Value to which the angle should be reset in degrees.
        """
        ...

    def speed(self) -> int:
        """
        Get the speed (angular velocity) of the motor.

        ----------
        Returns - Motor speed in degrees/second.
        """
        ...

    def stop(self, stop_type: Stop = Stop.COAST):
        """
        Stop the motor.

        ----------
        stop_type : Stop – Whether to coast, brake, or hold (Default: Stop.COAST).
        """
        ...

    def run(self, speed: int):
        """
        Keep the motor running at a constant speed (angular velocity). The motor will accelerate towards the requested speed and the duty cycle is automatically adjusted to keep the speed constant, even under some load. This continues in the background until you give the motor a new command or the program stops.

        ----------
        speed : float – Speed of the motor in degrees/second.
        """
        ...

    def run_time(self, speed: int, time: int, stop_type: Stop = Stop.COAST, wait: bool = True):
        """
        Run the motor at a constant speed (angular velocity) for a given amount of time. The motor will accelerate towards the requested speed and the duty cycle is automatically adjusted to keep the speed constant, even under some load. It begins to decelerate just in time to reach stand still after the specified duration.

        ----------
        speed : float - Speed of the motor (degrees/second).

        time : int – Duration of the maneuver (milliseconds).

        stop_type : Stop – Whether to coast, brake, or hold after coming to a stand still (Default: Stop.COAST).

        wait : bool – Wait for the maneuver to complete before continuing with the rest of the program (Default: True). This means that your program waits for the specified time.
        """
        ...

    def run_angle(self, speed: int, rotation_angle: int, stop_type: Stop = Stop.COAST, wait: bool = True):
        """
        Run the motor at a constant speed (angular velocity) by a given angle. The motor will accelerate towards the requested speed and the duty cycle is automatically adjusted to keep the speed constant, even under some load. It begins to decelerate just in time so that it comes to a stand still after traversing the given angle.

        ----------
        speed : float – Speed of the motor (degrees/second).

        rotation_angle : float – Angle by which the motor should rotate (degree).

        stop_type : Stop – Whether to coast, brake, or hold after coming to a stand still (Default: Stop.COAST).

        wait : bool – Wait for the maneuver to complete before continuing with the rest of the program (Default: True). This means that your program waits until the motor has traveled precisely the requested angle.
        """
        ...

    def run_target(self, speed: int, target_angle: int, stop_type: Stop = Stop.COAST, wait: bool = True):
        """
        Run the motor at a constant speed (angular velocity) towards a given target angle. The motor will accelerate towards the requested speed and the duty cycle is automatically adjusted to keep the speed constant, even under some load. It begins to decelerate just in time so that it comes to a stand still at the given target angle. The direction of rotation is automatically selected based on the target angle.

        ----------
        speed : float - Absolute speed of the motor (degrees/second). The direction will be automatically selected based on the target angle: it makes no difference if you specify a positive or negative speed.

        target_angle : float – Target angle that the motor should rotate to, regardless of its current angle (degrees).

        stop_type : Stop – Whether to coast, brake, or hold after coming to a stand still (Default: Stop.COAST).

        wait : bool – Wait for the maneuver to complete before continuing with the rest ofthe program (Default: True). This means that your program waits until the motor has reached the target angle.
        """
        ...

    def track_target(self, target_angle: int):
        """
        Track a target angle that varies in time. This function is quite similar to run_target(), but speed and acceleration settings are ignored: it will move to the target angle as fast as possible. Instead, you adjust speed and acceleration by choosing how fast or slow you vary the target_angle. This method is useful in fast loops where the motor target changes continuously.

        ----------
        target_angle : float – Target angle that the motor should rotate to (degrees).
        """
        ...

    def stalled(self) -> bool:
        """
        Check whether the motor is currently stalled. A motor is stalled when it cannot move even with the maximum torque. For example, when something is blocking the motor or your mechanism simply cannot turn any further. Specifically, the motor is stalled when the duty cycle computed by the PID controllers has reached the maximum (so duty=duty_limit) and still the motor cannot reach a minimal speed (so speed < stall_speed) for a period of at least stall_time. You can change the duty_limit, stall_speed,and stall_time settings using set_dc_settings() and set_pid_settings() in order to change the sensitivity to being stalled.

        ----------
        Returns - True if the motor is stalled, False if it is not.
        """
        ...

    def run_until_stalled(self, speed: int, stop_type: Stop = Stop.COAST, duty_limit: float = 100):
        """
        Run the motor at a constant speed (angular velocity) until it stalls. The motor is considered stalled when it cannot move even with the maximum torque. See stalled() for a more precise definition. The duty_limit argument lets you temporarily limit the motor torque during this maneuver. This is useful to avoid applying the full motor torque to a geared or lever mechanism.

        ----------
        speed : float - Speed of the motor (degrees/second).

        stop_type : Stop – Whether to coast, brake, or hold after coming to a stand still (Default: Stop.COAST).

        duty_limit : float - Relative  torque  limit as a percentage [0.0 to 100.0]. This limit works just like set_dc_settings(), but in this case the limit is temporary: it returns to its previous value after completing this command (Default: 100).
        """
        ...

    def set_dc_settings(self, duty_limit: float = 100, duty_offset: float = 0.0):
        """
        Configure the settings to adjust the behavior of the dc() command. This also affects all of the run commands, which use the dc() method in the background.

        ----------
        duty_limit : float - Relative torque limit during subsequent motor commands as a percentage [0.0 to 100.0]. This sets the maximum duty cycle that is applied during any subsequent motor command. This reduces the maximum torque output to a percentage of the absolute maximum stall torque. This is useful to avoid applying the full motor torque to a geared or lever mechanism, or to prevent your LEGO® train from unintentionally going at full speed. (Default: 100).

        duty_offset : float – Minimum duty cycle given when you use dc() as a percentage [0.0 to 100.0]. This adds a small feed forward torque so that your motor will move even for very low duty cycle values, which can be useful when you create your own feedback controllers (Default: 0).
        """
        ...

    def set_run_settings(self, max_speed: int, acceleration: int):
        """
        Configure the maximum speed and acceleration/deceleration of the motor for all run commands. This applies to the run, run_time, run_angle, run_target, or run_until_stalled commands you give the motor. See also the default parameters for each motor.

        ----------
        max_speed : float – Maximum speed of the motor during a motor command (degrees/second).

        acceleration : float –  Acceleration  towards  the  targetspeed and deceleration towards stand still (degrees/second/second). This should be a positive value. The motor will automatically change the sign to decelerate as needed.
        """
        ...

    def set_pid_settings(self, kp: int, ki: int, kd: int, tight_loop_limit: float, angle_tolerance: int, speed_tolerance: int, stall_speed: int, stall_time: int):
        """
        Configure the settings of the position and speed controllers. See also pid and the default parameters for each motor.

        ----------
        kp : int – Proportional position (and integral speed) control constant.

        ki : int – Integral position control constant.

        kd : int – Derivative position (and proportional speed) control constant. 

        tight_loop_limit : float – If you execute any of the run commands within this interval after starting the previous command, the controllers assume that you want to control the speed directly (ms). This means that it will ignore the acceleration setting and immediately begin tracking the speed you give in the run command. This is useful in a fast loop, where you usually want the motors to respond quickly rather than accelerate smoothly, for example with a line-following robot.

        angle_tolerance : float – Allowed deviation from the target angle before motion is considered complete (degrees).

        speed_tolerance : float – Allowed deviation from zero speed before motion is considered complete (deg/s).

        stall_speed : float – See stalled() (deg/s).

        stall_time : float - See stalled() (ms).
        """
        ...


class TouchSensor:
    """
    LEGO® MINDSTORMS® EV3 Touch Sensor. Element 95648/6138404, contained in:
    - 31313: LEGO® MINDSTORMS® EV3 (2013)
    - 45544: LEGO® MINDSTORMS® Education EV3 Core Set (2013)
    - 45507: Separate part (2013)
    """

    def __init__(self, port: Port):
        """
        LEGO® MINDSTORMS® EV3 Touch Sensor.

        ----------
        port : Port – Port to which the sensor is connected.
        """
        ...

    def pressed(self) -> bool:
        """
        Check if the sensor is pressed.

        ----------
        Returns - True if the sensor is pressed, False if it is not pressed.
        """
        ...


class ColorSensor:
    """
    LEGO® MINDSTORMS® EV3 Color Sensor. Element 95650/6128869, contained in:
    - 31313: LEGO® MINDSTORMS® EV3 (2013)
    - 45544: LEGO® MINDSTORMS® Education EV3 Core Set (2013)
    - 45506: Separate part (2013)
    """

    def __init__(self, port: Port):
        """
        LEGO® MINDSTORMS® EV3 Color Sensor.

        ----------
        port : Port – Port to which the sensor is connected.
        """
        ...

    def color(self) -> Color:
        """
        Measure the color of a surface.

        ----------
        Returns - Color.BLACK, Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED, Color.WHITE Color.BROWN or None.
        """
        ...

    def ambient(self) -> int:
        """
        Measure the ambient light intensity.

        ----------
        Returns - Ambient light intensity, ranging from 0 (dark) to 100 (bright).
        """
        ...

    def reflection(self) -> int:
        """
        Measure the reflection of a surface using a red light.

        ----------
        Returns - Reflection, ranging from 0 (no reflection) to 100 (high reflection).
        """
        ...

    def rgb(self) -> Tuple[float, float, float]:
        """
        Measure the reflection of a surface using a red, green, and then a blue light.

        ----------
        Returns - Reflection for red, green, and blue light, each ranging from 0.0 (no reflection) to 100.0(high reflection).
        """
        ...


class InfraredSensor:
    """
    LEGO® MINDSTORMS® EV3 Infrared Sensor and Beacon. Element 95654/6132629 and 72156/6127283, contained in:
    - 31313: LEGO® MINDSTORMS® EV3 (2013)
    - 45509 and 45508: Separate parts (2013)
    """

    def __init__(self, port: Port):
        """
        LEGO® MINDSTORMS® EV3 Infrared Sensor and Beacon. 

        ----------
        port : Port – Port to which the sensor is connected.
        """
        ...

    def distance(self) -> float:
        """
        Measure the relative distance between the sensor and an object using infrared light.

        ----------
        Returns - Relative distance ranging from 0 (closest) to 100 (farthest).
        """
        ...

    def beacon(self, channel: int) -> Tuple[float, float]:
        """
        Measure the relative distance and angle between the remote and the infrared sensor.

        ----------
        channel : int – Channel number of the remote.

        ----------
        Returns - Tuple of relative distance (0 to 100) and approximate angle (-75 to 75 degrees) between remote and infrared sensor or (None,None) if no remote is detected.
        """
        ...

    def buttons(self, channel: int) -> List[Button]:
        """
        Check which buttons on the infrared remote are pressed.

        ----------
        channel : int – Channel number of the remote.

        ----------
        Returns - List of pressed buttons on the remote on the specified channel.
        """
        ...


class UltrasonicSensor:
    """
    LEGO® MINDSTORMS® EV3 Ultrasonic Sensor. Element 95652/6138403, contained in:
    - 45544: LEGO® MINDSTORMS® Education EV3 Core Set (2013)
    - 45504: Separate part (2013)
    """

    def __init__(self, port: Port):
        """
        LEGO® MINDSTORMS® EV3 Ultrasonic Sensor.

        ----------
        port : Port – Port to which the sensor is connected.
        """
        ...

    def distance(self, silent: bool = False) -> int:
        """
        Measure the distance between the sensor and an object using ultrasonic sound waves.

        ----------
        silent : bool – Choose True to turn the sensor off after measuring the distance. Choose False to leave the sensor on (Default). When you choose silent=True, the sensor does not emit sounds waves except when taking the measurement. This reduces interference with other ultrasonic sensors, but turning the sensor off takes approximately 300 ms each time.

        ----------
        Returns - Distance (millimeters).
        """
        ...

    def presence(self) -> bool:
        """
        Check for the presence of other ultrasonic sensors by detecting ultrasonic sounds. If the other ultrasonic sensor is operating in silent mode, you can only detect the presence of that sensor while it is taking a measurement.

        ----------
        Returns - True if ultrasonic sounds are detected, False if not.
        """
        ...


class GyroSensor:
    """
    LEGO® MINDSTORMS® EV3 Gyro Sensor. Element 99380/6138411, contained in:
    - 45544: LEGO® MINDSTORMS® Education EV3 Core Set (2013)
    - 45505: Separate part (2013)
    """

    def __init__(self, port: Port, direction: Direction = Direction.CLOCKWISE):
        """
        LEGO® MINDSTORMS® EV3 Gyro Sensor.

        ----------
        port : Port – Port to which the sensor is connected.

        direction : Direction – Positive rotation direction when looking at the red dot on top of the sensor (Default: Direction.CLOCKWISE).
        """
        ...

    def speed(self) -> int:
        """
        Get the speed (angular velocity) of the sensor.

        ----------
        Returns - Sensor angular velocity (degrees/second).
        """
        ...

    def angle(self) -> int:
        """
        Get the accumulated angle of the sensor.

        ----------
        Returns - Rotation angle (degrees).
        """
        ...

    def reset_angle(self, angle: int):
        """
        Set the rotation angle of the sensor to a desired value.

        ----------
        angle : float – Value to which the angle should be reset in degrees.
        """
        ...
