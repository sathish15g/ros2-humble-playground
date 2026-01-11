#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class FrequencySubscriber(Node):
    def __init__(self):
        super().__init__('frequency_subscriber')
        self.declare_parameter('topic_name', '/chatter')

        topic_name = self.get_parameter('topic_name').get_parameter_value().string_value

        self.subscription = self.create_subscription(
            String,
            topic_name,
            self.listener_callback,
            10)
        self.get_logger().info(f'Subscriber listening on /{topic_name}')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    frequency_subscriber = FrequencySubscriber()
    rclpy.spin(frequency_subscriber)
    frequency_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()