import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty
import math
import time


class TurtleMotionController(Node):

    def __init__(self):
        super().__init__('turtle_motion_controller')
        self.get_logger().info('Turtle Motion Controller node initialized')

        # Publisher
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('Publisher created for /turtle1/cmd_vel')

        # Subscriber
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )
        self.get_logger().info('Subscribed to /turtle1/pose')

        # Service clients
        self.clear_client = self.create_client(Empty, '/clear')
        self.reset_client = self.create_client(Empty, '/reset')
        self.get_logger().info('Service clients created for /clear and /reset')

        self.pose = None

        self.wait_for_services()
        self.reset_turtle()

    def pose_callback(self, msg):
        self.pose = msg

    def wait_for_services(self):
        self.get_logger().info('Waiting for turtlesim services...')
        self.clear_client.wait_for_service()
        self.reset_client.wait_for_service()
        self.get_logger().info('Turtlesim services are available')

    def reset_turtle(self):
        self.get_logger().info('Clearing screen and resetting turtle to initial position')
        self.clear_client.call_async(Empty.Request())
        time.sleep(0.5)
        self.reset_client.call_async(Empty.Request())
        time.sleep(1.0)
        self.get_logger().info('Turtle reset completed')

    def move_linear(self, speed, duration):
        self.get_logger().info(
            f'Linear motion started | speed={speed}, duration={duration}s'
        )

        twist = Twist()
        twist.linear.x = speed

        start_time = time.time()
        while time.time() - start_time < duration:
            self.publisher.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(0.05)

        self.stop_robot()
        self.get_logger().info('Linear motion completed')

    def rotate_90_degrees(self):
        self.get_logger().info('Angular motion started (90 degree rotation)')

        while self.pose is None:
            rclpy.spin_once(self, timeout_sec=0.1)

        start_theta = self.pose.theta
        target_theta = self.normalize_angle(start_theta + math.pi / 2)

        self.get_logger().info(
            f'Rotation start theta={start_theta:.3f}, target theta={target_theta:.3f}'
        )

        twist = Twist()
        angular_speed = 0.5

        while True:
            rclpy.spin_once(self, timeout_sec=0.0)

            error = self.normalize_angle(target_theta - self.pose.theta)

            if abs(error) < 0.01:
                break

            twist.angular.z = angular_speed if error > 0 else -angular_speed
            self.publisher.publish(twist)
            time.sleep(0.05)

        self.stop_robot()
        self.get_logger().info('Angular motion completed (90 degrees)')

    def stop_robot(self):
        self.publisher.publish(Twist())
        time.sleep(0.3)
        self.get_logger().info('Robot stopped')

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def move_in_square(self):
        self.get_logger().info('Square motion started')

        for i in range(4):
            self.get_logger().info(f'Executing side {i + 1} of 4')
            self.move_linear(0.8, 2.0)
            self.rotate_90_degrees()

        self.get_logger().info('Perfect square completed successfully')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleMotionController()
    node.move_in_square()
    node.get_logger().info('Shutting down Turtle Motion Controller')
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
