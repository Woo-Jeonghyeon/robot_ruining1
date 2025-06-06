#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from picar_b2_base import RPIservo
from geometry_msgs.msg import Twist

class SteeringNode(Node):
    def __init__(self):
        super().__init__('steering_node')

        # 서보 제어 클래스 초기화
        self.servo = RPIservo.ServoCtrl()
        self.servo.moveInit()  # 기본 위치로 초기화

        # 제어할 서보 인덱스 (예: 0번 채널 → 서보 연결된 채널에 따라 변경 가능)
        self.servo_channel = 0
        self.offset = 57.0

        # ROS2 구독자 설정
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10
        )

        self.get_logger().info('Steering node initialized and listening to /servo_angle')

    def listener_callback(self, msg):
        angular_z = msg.angular.z
        
        # 제한 각도 클램핑
        angle = max(min(angular_z*45, 90.0), -90.0)
        actual_angle = self.offset + angle

        # 조향 서보 모터로 각도 전달
        self.servo.moveAngle(self.servo_channel, actual_angle)
        self.get_logger().info(f'Set steering angle to {angle:.2f} degrees (z={angular_z:.2f})')

def main(args=None):
    rclpy.init(args=args)
    node = SteeringNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

