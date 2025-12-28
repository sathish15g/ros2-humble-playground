#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class JokeSubscriber(Node):
    def __init__(self):
        super().__init__('joke_subscriber')

        self.subscription = self.create_subscription(
            String,
            '/programming_jokes',
            self.listener_callback,
            10
        )

        self.get_logger().info("😂 Joke Subscriber ready!")

    def listener_callback(self, msg):
        self.get_logger().info(f"📩 Heard: {msg.data}")
        print("😂 That's hilarious!")


def main(args=None):
    rclpy.init(args=args)
    node = JokeSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
