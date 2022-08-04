""" Example of a real and simulated robot"""

import time
from parameters_parser.parser import load_parameters
from common.data_structures import configuration
from common.interfaces import robot_interface
from real_robot.fossbot import FossBot as RealFossBot
from coppeliasim_robot.fossbot import FossBot as SimuFossBot

def main(robot: robot_interface.FossBotInterface) -> None:
    """ A simple robot routine """
    robot.just_move()
    time.sleep(10)
    robot.stop()

if __name__ == "__main__":
    # Load parameters from yml file
    file_parameters = load_parameters()

    # Create dataclass using file parameters
    parameters = configuration.RobotParameters(
        sensor_distance = configuration.SensorDistance(**file_parameters["sensor_distance"]),
        motor_left_speed= configuration.MotorLeftSpeed(**file_parameters["motor_left"]),
        motor_right_speed= configuration.MotorRightSpeed(**file_parameters["motor_right"]),
        default_step= configuration.DefaultStep(**file_parameters["step"]))

    # Create a real robot
    my_real_robot = RealFossBot(parameters= parameters)

    # Create a simu robot
    my_simu_robot = SimuFossBot(parameters= parameters)

    # Call a the same routine for the real and the simulated robot
    main(my_real_robot)

    main(my_simu_robot)
