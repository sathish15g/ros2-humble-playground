#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature
import random


class TemperaturePublisher(Node):
    """
    ROS 2 Temperature Publisher Node
    Publishes sensor_msgs/Temperature every 2 seconds
    """

    def __init__(self):
        super().__init__('temperature_publisher')
        self.publisher_ = self.create_publisher(
            Temperature,
            'my_temperature_topic',
            10
        )

        # Timer: 2 seconds publishing rate
        self.timer = self.create_timer(2.0, self.publish_temperature)

        self.get_logger().info('Temperature Publisher (sensor_msgs) started.')

    def publish_temperature(self):
        msg = Temperature()

        # Header (timestamp)
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'temperature_sensor_frame'

        # Simulated temperature value (°C)
        msg.temperature = round(random.uniform(25.0, 35.0), 2)
        msg.variance = 0.0

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Published Temperature: {msg.temperature} °C'
        )


def main(args=None):
    rclpy.init(args=args)

    node = TemperaturePublisher()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
