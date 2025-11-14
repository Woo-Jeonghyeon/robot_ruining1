#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from picar_b2_base import RPIservo

class SteeringNode(Node):
    def __init__(self):
        super().__init__('steering_node')
       
        self.servo = RPIservo.ServoCtrl()
        self.servo.moveInit()
       
        self.servo_channel = 0
        self.center_angle = 90.0
        self.min_angle = 50.0
        self.max_angle = 130.0
       
        # 비대칭 조향 범위 계산
        self.left_range = self.center_angle - self.min_angle   # 37.0°
        self.right_range = self.max_angle - self.center_angle  # 35.0°
       
        # 현재 각도
        self.current_angle = self.center_angle
        self.target_angle = self.center_angle
       
        # 제어 파라미터
        self.smoothing_factor = 0.3
        self.max_angle_change = 3.0
        self.dead_zone = 0.05
       
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10
        )
       
        self.timer = self.create_timer(0.02, self.update_servo)
       
        self.get_logger().info(
            f'Steering node initialized - Asymmetric range '
            f'(Left: {self.left_range:.1f}°, Right: {self.right_range:.1f}°)'
        )
   
    def listener_callback(self, msg):
        angular_z = msg.angular.z
       
        # Dead zone 적용
        if abs(angular_z) < self.dead_zone:
            angular_z = 0.0
       
        # 비대칭 각도 변환 (하드웨어 범위 최대 활용)
        if angular_z < 0:
            # 좌회전: -1.0 → -37.0°
            angle_offset = angular_z * self.left_range
        else:
            # 우회전: +1.0 → +35.0°
            angle_offset = angular_z * self.right_range
       
        # 타겟 각도 계산 및 제한
        self.target_angle = self.center_angle + angle_offset
        self.target_angle = max(min(self.target_angle, self.max_angle), self.min_angle)
   
    def update_servo(self):
        # 스무딩 적용
        desired_angle = (self.smoothing_factor * self.target_angle +
                        (1 - self.smoothing_factor) * self.current_angle)
       
        # 속도 제한 (ramping)
        angle_change = desired_angle - self.current_angle
       
        if abs(angle_change) > self.max_angle_change:
            if angle_change > 0:
                self.current_angle += self.max_angle_change
            else:
                self.current_angle -= self.max_angle_change
        else:
            self.current_angle = desired_angle
       
        # 서보 제어
        self.servo.moveAngle(self.servo_channel, self.current_angle)

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
