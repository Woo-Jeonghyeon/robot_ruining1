# RPIservo.py
import time
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class ServoCtrl:
    def __init__(self, channel=0, address=0x5f):
        self.channel = channel
        self.i2c = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.i2c, address=address)
        self.pca.frequency = 50
        self.servo = servo.Servo(self.pca.channels[self.channel], min_pulse=400, max_pulse=2700)
        self.servo.angle = 90  # 초기 각도

    def moveInit(self):
        self.servo.angle = 90

    def moveAngle(self, channel, angle):
        if channel != self.channel:
            self.servo = servo.Servo(self.pca.channels[channel], min_pulse=400, max_pulse=2700)
            self.channel = channel
        angle = max(min(angle, 130), 50)
        self.servo.angle = angle

    def cleanup(self):
        self.pca.deinit()

