import rclpy
from rclpy.node import Node
from rclpy.time import Time
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math


class FakeOdomPublisher(Node):
    def __init__(self):
        super().__init__('fake_dynamics_odom')

        # pub/sub
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10
        )

        self.br = TransformBroadcaster(self)

        # state
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0

        self.vx = 0.0
        self.delta = 0.0
        self.cmd_vx = 0.0
        self.cmd_wz = 0.0

        # params
        self.wheelbase = 0.12
        self.tau_v = 0.25
        self.tau_delta = 0.25
        self.max_steering_angle = math.radians(30)
        self.slip_factor = 0.03

        # timestamp
        self.last_time = self.get_clock().now()

        # timer
        self.timer = self.create_timer(0.02, self.timer_callback)

    def cmd_vel_callback(self, msg):
        self.cmd_vx = msg.linear.x
        self.cmd_wz = msg.angular.z

    def timer_callback(self):
        now = self.get_clock().now()

        # ---- Jazzy-safe dt 계산 방식 ----
        dt = (now.nanoseconds - self.last_time.nanoseconds) * 1e-9
        self.last_time = now

        if dt <= 0:
            return

        # ---- Ackermann Dynamics ----
        self.vx += (self.cmd_vx - self.vx) * (dt / self.tau_v)

        if abs(self.cmd_vx) < 1e-6:
            desired_delta = 0.0
        else:
            desired_delta = math.atan(self.cmd_wz * self.wheelbase / self.cmd_vx)

        desired_delta = max(-self.max_steering_angle,
                            min(self.max_steering_angle, desired_delta))

        self.delta += (desired_delta - self.delta) * (dt / self.tau_delta)

        tan_delta = math.tan(self.delta)
        if abs(tan_delta) < 1e-6:
            yaw_rate = 0.0
        else:
            yaw_rate = self.vx * tan_delta / self.wheelbase

        yaw_rate *= (1.0 - self.slip_factor * abs(self.vx))

        self.th += yaw_rate * dt
        self.th = math.atan2(math.sin(self.th), math.cos(self.th))

        self.x += self.vx * math.cos(self.th) * dt
        self.y += self.vx * math.sin(self.th) * dt

        # ---- Jazzy-safe timestamp ----
        stamp = now.to_msg()

        # ---- Publish /odom ----
        odom = Odometry()
        odom.header.stamp = stamp
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = math.sin(self.th / 2.0)
        odom.pose.pose.orientation.w = math.cos(self.th / 2.0)

        odom.twist.twist.linear.x = self.vx
        odom.twist.twist.angular.z = yaw_rate

        self.odom_pub.publish(odom)

        # ---- TF: odom → base_footprint ----
        t = TransformStamped()
        t.header.stamp = stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.z = math.sin(self.th / 2.0)
        t.transform.rotation.w = math.cos(self.th / 2.0)

        self.br.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = FakeOdomPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
