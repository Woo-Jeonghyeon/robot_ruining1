#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor

class MotorNode(Node):
    def __init__(self):
        super().__init__('motor_node')

        # ROS2 구독자 (cmd_vel에서 linear.x 값만 사용)
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )
       
        # I2C 및 모터 초기화
        i2c = busio.I2C(SCL, SDA)
        self.pwm_motor = PCA9685(i2c, address=0x5f)
        self.pwm_motor.frequency = 50

        self.motor1 = motor.DCMotor(self.pwm_motor.channels[15], self.pwm_motor.channels[14])  # M1 단일 구동 모터
        self.motor1.decay_mode = motor.SLOW_DECAY

        self.get_logger().info("Motor node started and listening to /cmd_vel")

    def map_speed(self, speed):
        return max(min(speed, 1.0), -1.0)

    def motor_stop(self):
        self.motor1.throttle = 0

    def cmd_vel_callback(self, msg):
        linear_speed = msg.linear.x

        speed = self.map_speed(linear_speed)

        self.motor1.throttle = speed

        self.get_logger().info(f"Set motor speed: {speed:.2f}")

    def destroy_node(self):
        self.motor_stop()
        self.pwm_motor.deinit()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    motor_node = MotorNode()
    try:
        rclpy.spin(motor_node)
    except KeyboardInterrupt:
        pass
    finally:
        motor_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()