from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='picar_b2_base',
            executable='motor_node',
            name='motor_node',
            output='screen'
        ),
        Node(
            package='picar_b2_base',
            executable='steering_node',
            name='steering_node',
            output='screen'
        ),
        Node(
            package='picar_b2_base',
            executable='ultrasonic_node',
            name='ultrasonic_node',
            output='screen'
        ),
        Node(
            package='picar_b2_base',
            executable='fake_odom_node',
            name='fake_odom_node',
            output='screen'
        )
    ])