#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature

class TempratureSubscriber(Node):
    """
    ROS 2 Temperature Subscriber Node
    Subscribes to sensor_msgs/Temperature messages
    topic: 'my_temperature_topic'
    
    Warnings if the temperature exceeds a certain threshold
    Alert: High temperature detected.
    """

    def __init__(self):
        super().__init__('temperature_subscriber')
        self.subscription = self.create_subscription(
            Temperature,
            'my_temperature_topic',
            self.temperature_callback,
            10
        )
        self.subscription  # prevent unused variable warning

        self.get_logger().info('Temperature Subscriber (sensor_msgs) started.')

    def temperature_callback(self, msg):
        self.get_logger().info(
            f'Received Temperature: {msg.temperature} °C'
        )
        if msg.temperature > 30.0:
            self.get_logger().warn('Alert: High temperature detected.')

    
def main(args=None):
    rclpy.init(args=args)
    temperature_subscriber = TempratureSubscriber()
    rclpy.spin(temperature_subscriber)
    temperature_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()