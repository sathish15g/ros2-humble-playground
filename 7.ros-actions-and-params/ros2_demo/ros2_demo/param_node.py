import rclpy
from rclpy.node import Node


class ParamNode(Node):
    def __init__(self):
        super().__init__('param_node')

        self.declare_parameter('robot_speed', 1.0)
        speed = self.get_parameter('robot_speed').value

        self.get_logger().info(f'Robot speed: {speed}')


def main():
    rclpy.init()
    node = ParamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
