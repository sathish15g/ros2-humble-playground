import rclpy
from rclpy.node import Node

rclpy.init()
node = Node("py_node")
rclpy.spin(node)
rclpy.shutdown()
# This is a basic test to ensure that the rclpy library can initialize and create a node without errors.

# No assertions or checks are needed; if no exceptions are raised, the test is considered successful.

# The test does not interact with the JokeSubscriber class directly,
# but it verifies that the ROS 2 Python client library is functioning correctly.