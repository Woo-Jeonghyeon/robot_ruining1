from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'picar_b2_base'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jh',
    maintainer_email='jh@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor_node = picar_b2_base.motor_node:main',
            'steering_node = picar_b2_base.steering_node:main',
            'ultrasonic_node = picar_b2_base.ultrasonic_node:main',
            'fake_odom_node = picar_b2_base.fake_odom_node:main',
        ],
    },
)
