
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleAngulaeMove(Node):

    def __init__(self):
        super().__init__('turtle_angular_move')
        self.publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.move_turtle)

    def move_turtle(self):
        twist = Twist()
        twist.linear.x = 1.0
        twist.angular.z = 1.0
        self.publisher.publish(twist)
        self.get_logger().info(f'Linear Velocity X: {twist.linear.x} ,  Y: {twist.linear.y} , Z: {twist.linear.z}')
        self.get_logger().info(f'Angular Velocity X: {twist.angular.x} ,  Y: {twist.angular.y} , Z: {twist.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    node = TurtleAngulaeMove()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()