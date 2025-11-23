from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, Command
from ament_index_python.packages import get_package_share_directory
import os

from launch_ros.parameter_descriptions import ParameterValue

robot_description = ParameterValue(
    Command([
        'xacro ',
        PathJoinSubstitution([
            FindPackageShare('picar_b2_base'),
            'urdf',
            'picar_b2.urdf.xacro'
        ])
    ]),
    value_type=str
)

def generate_launch_description():

    rplidar_dir = get_package_share_directory('rplidar_ros')

    return LaunchDescription([

        # ======================================================
        # 0. URDF → TF 생성기
        # ======================================================
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': False
            }],
            output='screen'
        ),

        # 만약 URDF에서 laser_frame 방향이 틀렸으면 여기서 보정 가능
        # 예) 90도 돌려야 하면: rpy="0 0 1.5708"
        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     arguments=['0', '0', '0', '0', '0', '1.5708', 'base_link', 'laser_frame']
        # ),

        # ======================================================
        # 1. RPLidar
        # ======================================================
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(rplidar_dir, 'launch', 'rplidar_a1_launch.py')
            ),
            launch_arguments={'serial_port': '/dev/ttyUSB0'}.items()
        ),

        # ======================================================
        # 2. BASE MOTOR / STEERING node
        # ======================================================
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

        # ======================================================
        # 3. Fake odom node
        # ======================================================
        Node(
            package='picar_b2_base',
            executable='fake_odom_node',
            name='fake_odom_node',
            output='screen'
        ),
        # Node(
        #     package='picar_b2_base',
        #     executable='scan_stamp_fixer',
        #     name='scan_stamp_fixer',
        #     output='screen'
        # ),
    ])
