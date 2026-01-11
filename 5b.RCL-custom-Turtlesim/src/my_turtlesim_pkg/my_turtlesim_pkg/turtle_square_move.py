
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleSquareMove(Node):

    def __init__(self):
        super().__init__('turtle_square_move')
        self.publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.move_turtle)
        self.side_count = 0
        self.state = 'move' # 'move' or 'turn'

    def move_turtle(self):
        twist = Twist()
        if self.state == 'move':
            twist.linear.x = 1.0
            self.publisher.publish(twist)
            self.get_logger().info(f'Moving Forward - Linear Velocity X: {twist.linear.x} ,  Y: {twist.linear.y} , Z: {twist.linear.z}')
            self.state = 'turn'
        elif self.state == 'turn':
            twist.angular.z = 1.57 # Approx 90 degrees in radians
            self.publisher.publish(twist)
            self.get_logger().info(f'Turning - Angular Velocity X: {twist.angular.x} ,  Y: {twist.angular.y} , Z: {twist.angular.z}')
            self.side_count += 1
            if self.side_count >= 4:
                self.get_logger().info('Completed square movement. Stopping turtle.')
                self.timer.cancel()
            else:
                self.state = 'move'

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSquareMove()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()