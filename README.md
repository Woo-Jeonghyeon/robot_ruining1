ros2_ws
# Autonomous Mobile Manipulator Robot

## Introduction

This project is a capstone design project focused on developing an autonomous mobile manipulator robot using ROS2 Humble.

The system integrates a mobile robot platform with an Arduino-based robotic arm using Raspberry Pi 5 as the main controller. The robot was designed to perform autonomous movement and robotic manipulation within a unified robotic system.

Through this project, practical experience was gained in robotic system integration, ROS2 communication architecture, embedded control systems, and mobile manipulation technologies.

---

## Main Features

- ROS2 Humble-based robotic system
- Autonomous mobile robot control
- Arduino-based robotic arm control
- Integration of mobile platform and manipulator
- Real-time node communication and control
- Sensor-based driving control

---

## System Configuration

### Hardware
- Raspberry Pi 5
- Arduino-based Robotic Arm
- Mobile Robot Chassis
- DC Motors
- Motor Driver
- Battery System
- Sensor Modules

### Software
- ROS2 Humble
- Python
- C++
- Ubuntu Linux
- Arduino IDE

---

## System Architecture

```text
Raspberry Pi 5 (ROS2 Humble)
│
├── Navigation Node
├── Motor Control Node
├── Sensor Node
└── Manipulator Interface Node
         │
         ▼
      Arduino
         │
         ▼
   Robotic Manipulator
```

---

## Project Objectives

- Develop an autonomous mobile robot platform
- Integrate a robotic arm with a mobile platform
- Implement a ROS2-based communication system
- Perform simultaneous navigation and manipulation tasks
- Gain practical experience in robotic system integration

---

## Results

- Successfully implemented autonomous mobile robot driving
- Achieved robotic arm control
- Integrated the mobile robot and manipulator system
- Implemented a ROS2-based real-time communication system

---

## How to Use

### 1. Clone Repository

```bash
git clone http://github.com/Woo-Jeonghyeon/robot_ruining1
```

### 2. Build ROS2 Workspace

```bash
colcon build
source install/setup.bash
```

### 3. Run

```bash
ros2 launch <package_name> <launch_file>.launch.py
```

---

## Project Images

Project images and demonstration videos will be uploaded later.

---

## Future Improvements

- SLAM-based autonomous navigation
- Object recognition system
- Camera-based vision system
- Remote control system
- Advanced path planning algorithms

---

## License

This project is licensed under the MIT License.

---

## Author

Woo Jeonghyeon

Mechanical Engineering

Capstone Design Project
