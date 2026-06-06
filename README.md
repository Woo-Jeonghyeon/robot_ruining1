ros2_ws

# Autonomous Mobile Manipulator Robot

## 📖 Overview

This project was developed as a Capstone Design Project to integrate autonomous navigation and robotic manipulation into a single robotic platform.

The system consists of a mobile robot driven by ROS2 Humble running on a Raspberry Pi 5 and an Arduino-based robotic manipulator. The objective was to develop a robot capable of autonomous movement while performing manipulation tasks through a robotic arm.

By combining mobility and manipulation, the project demonstrates the fundamental concept of a mobile manipulator system used in service robots, logistics robots, and autonomous robotic platforms.

---

## 🎯 Project Objectives

- Develop an autonomous mobile robot platform
- Integrate a robotic manipulator with a mobile base
- Implement ROS2-based communication architecture
- Perform coordinated navigation and manipulation tasks
- Gain practical experience in robotic system integration

---

## 🛠 Hardware

- Raspberry Pi 5
- Arduino-based Robotic Arm
- Mobile Robot Chassis
- DC Motors
- Motor Drivers
- Battery System
- Sensors for Navigation

---

## 💻 Software

- ROS2 Humble
- Ubuntu Linux
- Python
- C++
- Arduino IDE

---

## ⚙ System Architecture

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
