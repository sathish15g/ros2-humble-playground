import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from action_tutorials_interfaces.action import Fibonacci


class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')

        self._client = ActionClient(self, Fibonacci, 'fibonacci')

        # ✅ SEND GOAL AUTOMATICALLY
        self.send_goal()

    def send_goal(self):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = 10

        self.get_logger().info('Waiting for action server...')
        self._client.wait_for_server()

        self.get_logger().info('Sending goal...')
        self._send_goal_future = self._client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self._result_future = goal_handle.get_result_async()
        self._result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(
            f'Feedback: {feedback_msg.feedback.partial_sequence}'
        )


    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        self.destroy_node()



def main():
    rclpy.init()
    node = FibonacciActionClient()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

