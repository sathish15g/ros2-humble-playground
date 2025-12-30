import rclpy
from rclpy.node import Node

class ParamNode(Node):
    def __init__(self):
        super().__init__('param_node')
        # Declare a parameter with default value
        self.declare_parameter('robot_speed', 1.0)
        self.timer = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        speed = self.get_parameter('robot_speed').get_parameter_value().double_value
        self.get_logger().info(f'Current robot speed: {speed}')

def main(args=None):
    rclpy.init(args=args)
    node = ParamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
