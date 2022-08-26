"""
Implementation for control (dummy).
"""
import random
from common.interfaces import control_interfaces

MAX_RANGE = 1000

class Motor(control_interfaces.MotorInterface):
    """
    Motor() -> Motor control.
    Functions:
    dir_control(direction) Change motor direction to input direction.
    move(direction) Start moving motor with default speed towards input direction.
    set_speed(speed) Set speed immediately 0-100% range.
    stop() Stops the motor.
    """
    def __init__(self) -> None:
        print('Motor initialized.')

    def set_speed(self, speed: int) -> None:
        '''
        Set speed immediately 0-100% range.
        Param: speed: the range 0 - 100% that speed will be changed to.
        '''
        print('Speed set.')

    def dir_control(self, direction: str) -> None:
        '''
        Change motor direction to input direction.
        Param: direction: the direction to be headed to.
        '''
        print(f'Direction changed to {direction}.')

    def move(self, direction: str = "forward") -> None:
        '''
        Start moving motor with default speed towards input direction.
        Param: direction: the direction to be headed to.
        '''
        print(f'Moving {direction}.')

    def stop(self) -> None:
        '''Stops the motor.'''
        print('Stopping.')


class Odometer(control_interfaces.OdometerInterface):
    '''
    Class Odometer() -> Odometer control.
    Functions:
    count_revolutions() Increases the counter of revolutions.
    get_revolutions() Returns the number of revolutions.
    get_distance() Returns the traveled distance in cm.
    reset() Resets the steps counter.
    '''
    def __init__(self) -> None:
        print('Odometer initialized.')

    def count_revolutions(self) -> None:
        '''Increase total steps by one.'''
        print('Steps increased.')

    def get_steps(self) -> int:
        ''' Returns total number of steps. '''
        return random.randint(-MAX_RANGE, MAX_RANGE)

    def get_revolutions(self) -> float:
        ''' Returns total number of revolutions. '''
        return random.random()

    def get_distance(self) -> float:
        ''' Return the total distance traveled so far (in cm). '''
        return random.random()

    def reset(self) -> None:
        ''' Reset the total traveled distance and revolutions. '''
        print('Steps reset.')


class UltrasonicSensor(control_interfaces.UltrasonicSensorInterface):
    '''
    Class UltrasonicSensor() -> Ultrasonic sensor control.
    Functions:
    get_distance() return distance in cm.
    '''

    def __init__(self) -> None:
        print('Ultrasonic Sensor initialized.')

    def get_distance(self) -> float:
        '''
        Gets the distance to the closest obstacle.
        Returns: the distance to the closest obstacle (in cm).
        '''
        return random.random()


class AnalogueReadings(control_interfaces.AnalogueReadingsInterface):
    '''
    Class AnalogueReadings() -> Handles Analogue Readings.
    Functions:
    get_reading(pin) Gets reading of a specific sensor specified by input pin.
    '''

    def __init__(self) -> None:
        print('Analogue Reading initialized.')

    def get_reading(self, pin: int) -> float:
        '''
        Gets reading of a specific sensor specified by input pin.
        Param: pin: the pin of the sensor.
        Returns: the reading of the requested sensor.
        '''
        return random.random()


class LedRGB(control_interfaces.LedRGBInterface):
    '''
    Class LedRGB() -> Led control
    set_on(color): sets led to input color.
    '''

    def __init__(self) -> None:
        print('Led initialized.')

    def set_on(self, color: str) -> None:
        '''
        Changes the color of a led
        Param: color: the wanted color
        For closing the led, use color == 'closed'
        '''
        print(f'Color {color} set.')


class Accelerometer(control_interfaces.AccelerometerInterface):
    '''
    Class Accelerometer() -> Handles accelerometer and gyroscope.
    Functions:
    get_acceleration(dimension) Returns the acceleration for a specific dimension.
    get_gyro(dimension) Returns the gyroscope for a specific dimension.
    '''

    def __init__(self) -> None:
        print('Accelerometer/Gyroscope initialized.')

    def get_acceleration(self, dimension: str) -> float:
        '''
        Gets the acceleration for a specific dimension.
        Param: dimension: the dimension requested.
        Returns: the acceleration for a specific dimension.
        '''
        return random.random()


    def get_gyro(self, dimension: str) -> float:
        '''
        Gets gyroscope for a specific dimension.
        Param: dimension: the dimension requested.
        Returns: the gyroscope for a specific dimension.
        '''
        return random.random()
