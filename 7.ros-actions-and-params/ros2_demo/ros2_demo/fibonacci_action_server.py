from rclpy.node import Node
from rclpy.action import ActionServer
from action_tutorials_interfaces.action import Fibonacci
import rclpy
import time


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')

        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',  # ✅ SAME NAME
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback = Fibonacci.Feedback()
        sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            sequence.append(sequence[i] + sequence[i - 1])

            feedback.partial_sequence = sequence   # ✅ FIX
            goal_handle.publish_feedback(feedback)

            time.sleep(1)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = sequence
        return result




def main():
    rclpy.init()
    node = FibonacciActionServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
