"""
Real robot implementation
"""

import time
import subprocess
from common.data_structures import configuration
from common.interfaces import robot_interface
from coppeliasim_robot import control

try:
    from coppeliasim_robot import sim
except FileNotFoundError:
    print('--------------------------------------------------------------')
    print('"sim.py" could not be imported. This means very probably that')
    print('either "sim.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "sim.py"')
    print('--------------------------------------------------------------')
    print('')

def connect_vrep():
    '''
    Connects to Coppelia Server
    Returns: clientID
    '''
    print('Program started')
    sim.simxFinish(-1) # just in case, close all opened connections
    return sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5) # Connect to CoppeliaSim


class FossBot(robot_interface.FossBotInterface):
    """ Sim robot """
    def __init__(self, parameters: configuration.RobotParameters):
        self.client_id = connect_vrep()
        if self.client_id == -1:
            print('Failed connecting to remote API server')
            raise ConnectionError
        print('Connected to remote API server')
        self.parameters = parameters
        self.motor_left = control.Motor(self.client_id, "left_motor",
                                self.parameters.motor_left_speed.value)
        self.motor_right = control.Motor(self.client_id, "right_motor",
                                         self.parameters.motor_right_speed.value)
        self.ultrasonic = control.UltrasonicSensor(self.client_id)
        self.odometer_right = control.Odometer(self.client_id, "right_motor")
        self.odometer_left = control.Odometer(self.client_id, "left_motor")
        self.analogue_reader = control.AnalogueReadings(self.client_id)
        self.accelerometer = control.Accelerometer(self.client_id)
        self.rgb_led = control.Led_RGB(self.client_id)
        #self.noise = control.gen_input(pin=4)

    def get_distance(self) -> None:
        """ Return Distance in cm  """
        return self.ultrasonic.get_distance()

    def check_for_obstacle(self) -> None:
        """ Return if obstacle detected """
        i = self.ultrasonic.get_distance()
        if i <= self.parameters.sensor_distance.value:
            return True
        return False

    def just_move(self, direction="forward") -> None:
        """ Move forward forever """
        self.odometer_right.reset()
        self.odometer_left.reset()
        self.motor_right.move(direction=direction)
        self.motor_left.move(direction=direction)

    def stop(self) -> None:
        """ Stop moving """
        self.motor_left.stop()
        self.motor_right.stop()
        print('stop')
        self.odometer_right.reset()
        self.odometer_left.reset()

    def wait(self, time_s: int) -> None:
        time.sleep(time_s)

    def __del__(self):
        sim.simxFinish(self.client_id)

    def exit(self) -> None:
        sim.simxFinish(self.client_id)
        print('Program ended')

    def just_rotate(self, dir_id: int) -> None:
        self.odometer_right.reset()
        self.odometer_left.reset()
        left_dir = "reverse" if dir_id == 1 else "forward"
        right_dir = "reverse" if dir_id == 0 else "forward"
        self.motor_left.move(direction=left_dir)
        self.motor_right.move(direction=right_dir)

    #moving forward
    def move_forward_distance(self, dist: int) -> None:
        self.move_distance(dist)

    def move_forward_default(self) -> None:
        self.move_distance(self.parameters.default_step.value)

    def rotate_clockwise(self) -> None:
        self.just_rotate(1)

    def rotate_counterclockwise(self) -> None:
        self.just_rotate(0)

    def move_forward(self) -> None:
        self.just_move()

    def rotate_clockwise_90(self) -> None:
        self.rotate_90(1)

    def rotate_counterclockwise_90(self) -> None:
        self.rotate_90(0)

    #moving reverse
    def move_reverse_distance(self, dist: int) -> None:
        self.move_distance(dist, direction="reverse")

    def move_reverse_default(self) -> None:
        self.move_distance(self.parameters.default_step.value, direction="reverse")

    def move_reverse(self) -> None:
        self.just_move(direction="reverse")

    def rotate_90(self, dir_id: int) -> None:
        self.just_rotate(dir_id)
        rotations = self.parameters.rotate_90.value
        steps_r = self.odometer_right.get_steps()
        steps_l = self.odometer_left.get_steps()
        while steps_r <= rotations and steps_l <= rotations:
            steps_r = self.odometer_right.get_steps()
            steps_l = self.odometer_left.get_steps()
            time.sleep(0.01)
        self.stop()

    def move_distance(self, dist, direction: str = "forward") -> None:
        if dist == 0:
            return
        self.just_move(direction=direction)
        dis_run_r = self.odometer_right.get_distance()
        dis_run_l = self.odometer_left.get_distance()
        while dis_run_r < dist and dis_run_l < dist:
            dis_run_r = self.odometer_right.get_distance()
            dis_run_l = self.odometer_left.get_distance()
        self.stop()

    def reset_dir(self) -> None:
        self.motor_left.dir_control("forward")
        self.motor_right.dir_control("forward")

    #sound
    def play_sound(self, audio_id: int) -> None:
        audio_id = int(audio_id)
        if audio_id == 1:
            subprocess.run(["mpg123", "../robot_lib/soundfx/geia.mp3"], check=True)
        elif audio_id == 2:
            subprocess.run(["mpg123", "../robot_lib/soundfx/mpravo.mp3"], check=True)
        elif audio_id == 3:
            subprocess.run(["mpg123", "../robot_lib/soundfx/empodio.mp3"], check=True)
        elif audio_id == 4:
            subprocess.run(["mpg123", "../robot_lib/soundfx/kalhmera.mp3"], check=True)
        elif audio_id == 5:
            subprocess.run(["mpg123", "../robot_lib/soundfx/euxaristw.mp3"], check=True)
        elif audio_id == 6:
            subprocess.run(["mpg123", "../robot_lib/soundfx/r2d2.mp3"], check=True)
        elif audio_id == 7:
            subprocess.run(["mpg123", "../robot_lib/soundfx/machine_gun.mp3"], check=True)

    def get_floor_sensor(self, sensor_id: int) -> list:
        '''
        Floor Sensors
        '''
        return self.analogue_reader.get_reading(sensor_id)

    def check_on_line(self, sensor_id: int) -> bool:
        if sensor_id not in [1, 2, 3]:
            print(f'Sensor id {sensor_id} is out of bounds.')
            raise RuntimeError

        # [23, 23, 23] => black line
        if sensor_id == 3:
            if self.analogue_reader.get_reading(sensor_id) == [23, 23, 23]:
                return True
        elif sensor_id == 1:
            if self.analogue_reader.get_reading(sensor_id) == [23, 23, 23]:
                return True
        elif sensor_id == 2:
            if self.analogue_reader.get_reading(sensor_id) == [23, 23, 23]:
                return True
        return False

    def get_acceleration(self, axis: str = 'all') -> dict:
        value = self.accelerometer.get_acceleration(dimension=axis)
        print(value)
        return value

    def get_gyroscope(self, axis: str = 'all') -> dict:
        value = self.accelerometer.get_gyro(dimension=axis)
        print(value)
        return value

    #rgb
    def rgb_set_color(self, color: str) -> None:
        self.rgb_led.set_on(color)

    def __transf_1024(self, value: float) -> float:
        return value * 1024

    #light sensor
    def get_light_sensor(self) -> float:
        return self.__transf_1024(self.analogue_reader.get_reading(0))

    def check_for_dark(self) -> bool:
        # grey == 50%, white == 100%, black <= 10%
        grey_color = self.parameters.light_sensor.value / 1024
        value = self.analogue_reader.get_reading(0)
        print(self.__transf_1024(value))
        return bool(value < grey_color)

    #!FIXME
    def get_noise_detection(self) -> bool:
        # do it with microphone (real hw)
        pass
