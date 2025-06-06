import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from gpiozero import DistanceSensor
from time import sleep

class UltraNode(Node):
    def __init__(self):
        super().__init__('ultra_node')
        self.publisher_ = self.create_publisher(Float32, 'ultrasonic_distance', 10)
       
        Tr = 23
        Ec = 24
        self.sensor = DistanceSensor(echo=Ec, trigger=Tr, max_distance=2)

        # 타이머 20ms 마다 콜백 호출
        self.timer = self.create_timer(0.02, self.timer_callback)

    def timer_callback(self):
        distance = self.sensor.distance * 100  # cm 단위
        msg = Float32()
        msg.data = float(distance)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Ultrasonic Distance: {distance:.2f} cm')

def main(args=None):
    rclpy.init(args=args)
    ultra_node = UltraNode()
    rclpy.spin(ultra_node)
    ultra_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

