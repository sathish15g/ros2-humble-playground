#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class FrequencyPublisher(Node):
    def __init__(self):
        super().__init__('frequency_publisher')
        self.declare_parameter('frequency', 1.0)
        self.declare_parameter('topic_name', '/chatter')

        topic_name = self.get_parameter('topic_name').get_parameter_value().string_value
        frequency = self.get_parameter('frequency').get_parameter_value().double_value

        self.publisher_ = self.create_publisher(String, topic_name, 10)
        timer_period = 1.0 / frequency  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info(f'Lauching Publisher on /{topic_name} at {frequency} Hz')

    def timer_callback(self):
        msg = String()
        msg.data = 'System OK'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    frequency_publisher = FrequencyPublisher()
    rclpy.spin(frequency_publisher)
    frequency_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()