import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ColorDetector(Node):
    def __init__(self):
        super().__init__('color_detector')
        self.subscription = self.create_subscription(Image, '/camera/image_raw', self.listener_callback, 10)
        self.bridge = CvBridge()

    def listener_callback(self, data):
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        hsv_frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Detection ranges
        red_mask = cv2.inRange(hsv_frame, np.array([0, 100, 100]), np.array([10, 255, 255]))
        green_mask = cv2.inRange(hsv_frame, np.array([40, 40, 40]), np.array([80, 255, 255]))

        if np.sum(red_mask) > 10000: self.get_logger().info('IDENTIFIED: RED TARGET')
        if np.sum(green_mask) > 10000: self.get_logger().info('IDENTIFIED: GREEN TARGET')

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(ColorDetector())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
